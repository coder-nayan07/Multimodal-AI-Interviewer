import { useRef, useState, useCallback } from 'react';

// 1. Define the Feedback Type
type Feedback = {
  score: number;
  feedback: string;
};

type Message = {
  role: 'ai' | 'user';
  content: string;
};

// Replace the default string below with your actual ngrok URL 
// Example: "wss://cloacal-heike-graspable.ngrok-free.dev/api/v1/ws/interview/web_user_1"
export const useInterviewSocket = (
  url = "ws://localhost:9001/api/v1/ws/interview/web_user_1"
) => {
  const [messages, setMessages] = useState<Message[]>([]);
  
  // 2. Add State for Feedback
  const [lastFeedback, setLastFeedback] = useState<Feedback | null>(null);
  
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    // Prevent multiple connections
    if (socketRef.current?.readyState === WebSocket.OPEN) return;

    console.log("Connecting to WebSocket:", url);
    const ws = new WebSocket(url);
    socketRef.current = ws;

    ws.onopen = () => {
        console.log("WebSocket Connected");
        setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      // Handle AI Responses
      if (data.type === 'ai_response') {
        setMessages((prev) => [...prev, { role: 'ai', content: data.payload }]);
      }
      
      // 3. Handle Feedback Events
      if (data.type === 'feedback') {
        console.log("Got Feedback:", data.payload); // Debug log
        setLastFeedback(data.payload);
      }
    };

    ws.onclose = () => {
        console.log("WebSocket Disconnected");
        setIsConnected(false);
    };
    
    ws.onerror = (error) => {
        console.error("WebSocket Error:", error);
    };
    
  }, [url]);

  const sendMessage = (text: string) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      setMessages((prev) => [...prev, { role: 'user', content: text }]);
      socketRef.current.send(JSON.stringify({ type: 'answer', payload: text }));
      
      // Clear old feedback when answering a new question
      setLastFeedback(null); 
    } else {
        console.warn("Cannot send message: WebSocket is not open");
    }
  };

  const uploadResume = (fileName: string) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: 'init', payload: fileName }));
    } else {
        console.warn("Cannot upload resume: WebSocket is not open");
    }
  };

  // 4. Return lastFeedback so page.tsx can use it
  return { messages, lastFeedback, isConnected, sendMessage, uploadResume, connect };
};