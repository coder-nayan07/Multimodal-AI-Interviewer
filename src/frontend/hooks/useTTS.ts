import { useState, useCallback, useRef, useEffect } from 'react';

export const useTTS = () => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Cleanup: Stop audio if the user leaves the page
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
      }
    };
  }, []);

  const speak = useCallback((audioUrl: string) => {
    // 1. Sanity Check
    if (!audioUrl) {
      console.error(" useTTS: Received empty audio URL.");
      return;
    }

    // 2. Stop any previous audio
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }

    // 3. Construct the Full URL
    // FIXED: Changed to 9001 to match your SSH tunnel (9001 -> Server 8000)
    const backendUrl = "http://localhost:9001"; 
    
    // If the URL is relative (starts with /), add the backend domain
    const fullUrl = audioUrl.startsWith("http") 
      ? audioUrl 
      : `${backendUrl}${audioUrl}`;
    
    console.log("🔊 Playing Audio from:", fullUrl);

    // 4. Play the MP3
    const audio = new Audio(fullUrl);
    audioRef.current = audio;
    setIsSpeaking(true);

    audio.play()
      .then(() => console.log("Audio started"))
      .catch((err) => console.error(" Audio Playback Failed:", err));

    audio.onended = () => setIsSpeaking(false);
    
    audio.onerror = (e) => {
        console.error(" Audio Load Error. Check your Port/Network:", e);
        setIsSpeaking(false);
    };

  }, []);

  const stop = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsSpeaking(false);
    }
  }, []);

  return { speak, stop, isSpeaking };
};