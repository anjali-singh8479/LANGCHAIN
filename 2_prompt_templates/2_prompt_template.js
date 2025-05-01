import { ChatOpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { HumanMessage } from "@langchain/core/messages";
import dotenv from "dotenv";
import readlineSync from "readline-sync";


dotenv.config();

const chat_openai = new ChatOpenAI({
  model: "gpt-4o",
  temperature: 0.7,
  apiKey: process.env.OPENAI_API_KEY,
});

const chatprompt = new PromptTemplate({
  template: "Hi, I will help to get the {language} word for a given English word. What is a {language} word for {word}?",
  inputVariables: ["word", "language"],
});

async function getWord() {
  while (true) {
    const word = readlineSync.question("Enter the word: ");
    if (word.toLowerCase() === "exit") {
      console.log("Exiting the program.");
      process.exit(0);
    }
    const language = readlineSync.question("Enter the language: ");
    const formattedPrompt = await chatprompt.format({ word, language });

    const response = await chat_openai.invoke([
      new HumanMessage(formattedPrompt),
    ]);

    console.log("AI:", response.content);
  }
}

getWord();
