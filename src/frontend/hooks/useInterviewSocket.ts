import { useEffect, useRef, useState } from 'react';
import { useTTS } from './useTTS'; // <--- 1. Import the Audio Hook

// --- CRITICAL FIX: Port 9001 ---
// Since your SSH tunnel maps 9001 -> 8000, we must connect to 9001 here.
const WS_URL = "ws://localhost:9001/api/v1/ws/interview/web_user_1";

export const useInterviewSocket = () => {
  const { speak } = useTTS(); // Initialize the player
  
  const [messages, setMessages] = useState<any[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [lastFeedback, setLastFeedback] = useState<any>(null);

  const ws = useRef<WebSocket | null>(null);

  const connect = () => {
    if (ws.current) return;

    console.log("🔌 Connecting to WebSocket at:", WS_URL);
    const socket = new WebSocket(WS_URL);
    ws.current = socket;

    socket.onopen = () => {
      console.log(" WebSocket Connected");
      setIsConnected(true);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // Case 1: AI Responds (Text + Audio)
        if (data.type === 'ai_response') {
          // Add text bubble
          setMessages((prev) => [...prev, { role: 'ai', content: data.payload }]);
          setIsProcessing(false);

          // --- AUDIO TRIGGER ---
          if (data.audio) {
            console.log("🎤 Triggering Audio:", data.audio);
            speak(data.audio); // <--- Plays the MP3
          }
        }
        
        // Case 2: Feedback/Score
        else if (data.type === 'feedback') {
          console.log(" Got Feedback:", data.payload);
          setLastFeedback(data.payload);
        }

      } catch (err) {
        console.error(" Error parsing websocket message:", err);
      }
    };

    socket.onclose = () => {
      console.log("⚠️ WebSocket Disconnected");
      setIsConnected(false);
      ws.current = null;
    };

    socket.onerror = (error) => {
      console.error(" WebSocket Error:", error);
    };
  };

  // Send Message Function
  const sendMessage = (text: string, type: 'init' | 'answer' = 'answer') => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      // Add user message to UI immediately
      if (type === 'answer') {
        setMessages((prev) => [...prev, { role: 'user', content: text }]);
      }
      
      setIsProcessing(true);
      
      // Send to Backend
      ws.current.send(JSON.stringify({ type, payload: text }));
    } else {
      console.error(" Cannot send message: WebSocket is not open.");
    }
  };

  // Auto-connect on mount
  useEffect(() => {
    connect();
    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  return { 
    messages, 
    sendMessage, 
    isConnected, 
    isProcessing, 
    lastFeedback 
  };
};