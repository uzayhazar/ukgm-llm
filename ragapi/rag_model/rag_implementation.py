from typing import Any

import numpy as np

import torch
from transformers import GPTJForCausalLM, GPT2Tokenizer
from langchain_huggingface import HuggingFaceEmbeddings

from rag_model.generate_vectors import Vectorizer
# from generate_vectors import Vectorizer


class RAGChat:
    def __init__(self, query, **kwargs: Any):
        """Initialize the RAGChat."""
        self.query = query

    def vector_search(self):
        vectorizer = Vectorizer()
        vectorstore, doc_texts = vectorizer.create_faiss_vectorstore()

        embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        # if not self.query:
        #     self.query = "Was sind Risikofaktoren für Mundhöhlenkarzinom?"
        query_embedding = np.array(embedding_model.embed_query(self.query))

        # Reshape the query embedding
        query_embedding = query_embedding.reshape(1, -1)  # Shape: (1, 384)

        # Perform similarity search in the vector store
        k = 5  # Number of top results
        distances, indices = vectorstore.search(query_embedding, k)

        # Retrieve top matching documents
        result_doc = [doc_texts[idx] for idx in indices[0]]
        print("Top matching documents:")
        for i, doc in enumerate(result_doc):
            print(f"Rank {i+1}: {doc} (Distance: {distances[0][i]})")
        return result_doc


    def preprocess_context(self, result_doc):
        # Remove excessive whitespace and strip each document
        cleaned_context = [doc.strip() for doc in result_doc if doc.strip()]  # Remove empty entries
        # Join the cleaned lines with clear separation for readability
        return " ".join(cleaned_context)
    

    # Function to generate a response
    def generate_response_with_gptj(self):
        """
        Generate a response using GPT-J with a query and context.
        """
        
        result_doc = self.vector_search()
        # Combine the result_doc into a context
        context = self.preprocess_context(result_doc)

        # Create the prompt
        prompt = f"""
        Du bist ein Arzt und wirst von einem Patienten etwas gefragt. Du bekommst außerdem einen Kontext von relevanten medizinisch genauen Aussagen, welche du verwenden sollst, um eine Antwort zu formulieren.
        
        Anweisungen:
        - Sei hilfreich und beantworte die Frage so genau wie möglich.
        - Nutze den Kontext der dir gegeben wird für genaue und spezielle Informationen.
        - Antworte auf einfache Fragen so kurz und einfach wie möglich, nutze hierfür nur die relevantesten Teile des dir gegebenen Kontexts.
        - Gib für umfangreichere Fragen mehr Informationen aus dem dir gegebenen Kontext.
        
        Kontext: {context}
        Frage: {self.query}
        """

        # Load GPT-J model and tokenizer
        # model_name = "EleutherAI/gpt-j-6B"
        # tokenizer = GPT2Tokenizer.from_pretrained(model_name)

        # # Add a pad token if missing
        # if tokenizer.pad_token is None:
        #     tokenizer.pad_token = tokenizer.eos_token  # Use eos_token as pad_token


        # Load the model and move to the correct device
        # model = GPTJForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto", offload_folder="./offload")

        # # Tokenize the input manually
        # #inputs = tokenizer.encode(prompt,return_tensors="pt", truncation=True,max_length=1024).to("cuda" if torch.cuda.is_available() else "cpu")
        # inputs = tokenizer(
        #     prompt,
        #     return_tensors="pt",
        #     # padding=True,
        #     truncation=True,
        #     max_length=1024
        # ).to("cuda" if torch.cuda.is_available() else "cpu")

        # # import pdb;pdb.set_trace()

        # # Generate the output
        # output = model.generate(
        #     input_ids=inputs["input_ids"],
        #     # attention_mask=inputs["attention_mask"],  # Pass attention mask explicitly
        #     max_length=900,  # Set max response length
        #     temperature=0.7,  # Adjust for diverse outputs
        #     top_p=0.9,  # Top-p nucleus sampling
        #     do_sample=True,  # Enable sampling
        # )

        # # Decode the output
        # response = tokenizer.decode(output[0], skip_special_tokens=True)
        # return response.strip()
        from groq import Groq

        client = Groq(
            api_key="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"
        )

        chat_completion = client.chat.completions.create(
            messages = [
                {
                    "role":"user",
                    "content":f"{prompt}"
                }
            ],
            model = "llama-3.3-70b-versatile",
            # model = "mixtral-8x7b-32768",
        )

        print(chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content

# Generate the response
# response = generate_response_with_gptj(query, result_doc)
# print("\nGenerated Response:\n", response)

# To run separately, uncomment below and don't forget to use proper imports
# rag = RAGChat( query = "Was sind Risikofaktoren für Mundhöhlenkarzinom?")
# response = rag.generate_response_with_gptj()
# print("\nGenerated Response:\n", response)
