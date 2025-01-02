import os
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
import openai

class ActionProvideClause(Action):
    def name(self) -> Text:
        return "action_provide_clause"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Step 1: Get the last user message
        user_question = tracker.latest_message['text']
        if not user_question:
            dispatcher.utter_message(text="I couldn't find the question context. Please provide more details.")
            return []

        # Step 2: Load precomputed embeddings and metadata

        # Get the absolute path of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct paths for the files
        embeddings_path = os.path.join(current_dir, "clause_embeddings.npy")
        metadata_path = os.path.join(current_dir, "clause_metadata.json")
        
        try:
            loaded_clause_embeddings = np.load(embeddings_path)
            loaded_clause_metadata = json.load(open(metadata_path, "r"))
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: Precomputed embeddings or metadata file not found.")
            return []

        # Step 3: Convert embeddings to tensor
        clause_embeddings_tensor = torch.tensor(loaded_clause_embeddings)

        # Step 4: Load embedding model and compute embedding for user question
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        user_embedding = embedding_model.encode(user_question, convert_to_tensor=True)

        # Step 5: Compute cosine similarity and get top 3 matches
        similarities = util.cos_sim(user_embedding, clause_embeddings_tensor)
        top_indices = similarities[0].argsort(descending=True)[:3]
        top_clauses = [loaded_clause_metadata[idx] for idx in top_indices]

        # Step 6: Create example text for the prompt
        example_text = "\n\n".join(
            [f"Example {i+1}:\n{clause['text']}" for i, clause in enumerate(top_clauses)]
        )

        # Step 7: Create the OpenAI prompt
        prompt = (
            f"Context: {user_question}\n\n"
            f"Here are some examples of clauses:\n\n"
            f"{example_text}\n\n"
            "Task: Based on the context and examples, draft a clause tailored to this contract.\n\nClause:\n"
        )

        # Step 8: Call OpenAI API
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            dispatcher.utter_message(text="Error: OpenAI API key is not set.")
            return []

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a legal expert drafting contractual clauses."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.5,
            )
            generated_text = response.choices[0].message.content
        except Exception as e:
            dispatcher.utter_message(text=f"Error while generating clause: {str(e)}")
            return []

        # Step 9: Send response to the user
        dispatcher.utter_message(text=f"Here is your tailored clause:\n\n{generated_text}\n\n"
                 f"Examples used:\n\n{example_text}")

        return []
