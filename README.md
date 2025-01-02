# SmartClauseAI

SmartClauseAI is a Retrieval-Augmented Generation (RAG) framework designed to assist in legal document drafting and analysis. By leveraging the CUAD (Contract Understanding Atticus Dataset), the system retrieves relevant clauses and generates context-aware legal clauses tailored to specific situations. It integrates seamlessly with Rasa, an open-source conversational AI framework, and uses state-of-the-art models like **GPT-3.5 Turbo** and **MiniLM v6** for clause generation and retrieval. The project is fully containerized using Docker for streamlined deployment.

## Features

- **Clause Retrieval**: Retrieves the top 3 relevant clauses from the CUAD dataset using **MiniLM v6** for embedding-based semantic search.
- **Clause Generation**: Generates new legal clauses customized to specific scenarios using **GPT-3.5 Turbo**.
- **Conversational Interface**: Provides a user-friendly chatbot interface for clause interaction and customization.
- **Seamless Deployment**: Fully automated with Docker, eliminating the need for manual setup.

## Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Krishna-PriyaG/SmartClauseAI.git
   cd SmartClauseAI
Start the Application Start the application using Docker Compose:

bash
docker-compose up
This command will:

Train the Rasa model (if not already trained).
Start the Rasa server.
Start the action server.
Deploy the UI.
Access the Application

Chatbot (UI): http://localhost:8000
Rasa Server: http://localhost:5005
Action Server: http://localhost:5055
Usage
Interact with the Bot

Open the UI at http://localhost:8000 to interact with the bot.
Alternatively, use the Rasa shell for direct interaction:
bash
Copy code
docker exec -it <container_id> rasa shell
Supported Features

Retrieve relevant clauses from the CUAD dataset.
Generate new clauses tailored to specific legal scenarios.
Project Structure
actions/: Contains custom actions for retrieval and generation logic.
data/: Training data for the Rasa bot.
models/: Pre-trained and generated models for Rasa and clause generation.
config.yml: Configuration for the Rasa bot pipeline and policies.
domain.yml: Rasa bot domain definition.
docker-compose.yml: Docker configuration for containerized deployment.
ui/: Contains frontend assets for the chatbot interface.
Technologies Used
Rasa: Open-source conversational AI framework.
CUAD Dataset: Contract Understanding Atticus Dataset for legal clause retrieval.
GPT-3.5 Turbo: For generating context-aware legal clauses.
MiniLM v6: For efficient clause retrieval using embeddings.
Docker: For fully automated and containerized deployment.
Python: Programming language for backend logic.
Contributions
Contributions are welcome! Please open an issue or submit a pull request.
