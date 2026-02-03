import { useState, useCallback, useRef } from 'react';

export const useSpeech = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  
  // Store the recognition instance so we can stop it manually
  const recognitionRef = useRef<any>(null);

  const startListening = useCallback(() => {
    if (typeof window === 'undefined') return;

    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert("Browser does not support speech recognition. Try Chrome.");
      return;
    }

    // @ts-ignore
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    // CRITICAL FIX: Keep listening even if user pauses
    recognition.continuous = true; 
    recognition.interimResults = true; // Show words as you speak
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event: any) => {
      let finalTranscript = "";
      // Loop through results to handle continuous stream
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        }
      }
      if (finalTranscript) {
        setTranscript((prev) => prev + " " + finalTranscript);
      }
    };

    recognition.onerror = (event: any) => {
      console.log("Speech Error:", event.error); // Safe to log for debugging
      if (event.error === 'not-allowed') setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  }, []);

  return { isListening, transcript, startListening, stopListening, setTranscript };
};