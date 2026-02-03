import { useRef, useState, useCallback } from 'react';

type Message = {
  role: 'ai' | 'user';
  content: string;
};

export const useInterviewSocket = (url: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (socketRef.current?.readyState === WebSocket.OPEN) return;

    console.log("Connecting to WS:", url);
    const ws = new WebSocket(url);
    socketRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      console.log("✅ WebSocket Connected");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'ai_response') {
        setMessages((prev) => [...prev, { role: 'ai', content: data.payload }]);
      }
    };

    ws.onclose = () => setIsConnected(false);
  }, [url]);

  const sendMessage = (text: string) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      setMessages((prev) => [...prev, { role: 'user', content: text }]);
      socketRef.current.send(JSON.stringify({
        type: 'answer',
        payload: text
      }));
    }
  };

  const uploadResume = (fileName: string) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({
        type: 'init',
        payload: fileName
      }));
    }
  };

  return { messages, isConnected, sendMessage, uploadResume, connect };
};