import{ initializeApp, cert } from "firebase-admin/app"
import { getFirestore } from "firebase-admin/firestore";
import OpenAI from "openai"
import readline from "readline-sync";
import dotenv from "dotenv"
import fs from 'fs';
import readlineSync from 'readline-sync';
import {ChatOpenAI} from "@langchain/openai";
// Read and parse the JSON manually
const serviceAccount = JSON.parse(fs.readFileSync('../firebaseKey.json', 'utf-8'));



dotenv.config();

// Initialize Firebase Admin SDK
initializeApp({
  credential: cert(serviceAccount)
});

const db = getFirestore();

// OpenAI setup
const openai=new ChatOpenAI({model:"gpt-4o-mini"})

// Session setup
const sessionId = "user_chat_session_" + new Date().toISOString();
const collectionName = "Langchain_user_chats";

console.log("Session ID:", sessionId);

// Store chat history
const chatHistory = [];

async function chatLoop() {
  while (true) {
const userInput = readlineSync.question("You :");
    if (userInput.toLowerCase() === "end") break;

    chatHistory.push({ role: "user", content: userInput });

    const response=await openai.invoke(chatHistory);

    const aiMessage= response.content
    console.log("AI :", aiMessage);

    chatHistory.push({ role: "assistant", content: aiMessage });

    // Store both messages in Firestore
    
    }
    await db.collection(collectionName).add({
        session_id: sessionId,
        timeStamp:new Date(),
        messages: chatHistory,
    })
  console.log("Chat ended. Conversation saved to Firestore.");
}

chatLoop();

// this is using openai module
// const openai = new OpenAI({
//     apiKey: process.env.OPENAI_API_KEY,
//   });
// const response = await openai.chat.completions.create({
    //     model: "gpt-4o-mini",
    //     messages: chatHistory,
    //   });
    
    // const aiMessage=response.choices[0].message.content;
