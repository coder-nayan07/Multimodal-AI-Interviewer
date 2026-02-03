import { useState, useCallback, useEffect } from 'react';

export const useTTS = () => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

  // 1. Load Voices Asynchronously
  useEffect(() => {
    const loadVoices = () => {
      const available = window.speechSynthesis.getVoices();
      setVoices(available);
    };

    loadVoices();
    
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
  }, []);

  const speak = useCallback((text: string) => {
    if (!window.speechSynthesis) return;

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    
    // 2. Select a Voice
    const preferredVoice = voices.find(
      v => v.name.includes("Google US English") || v.name.includes("Zira")
    );
    
    if (preferredVoice) utterance.voice = preferredVoice;
    
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    
    // FIXED: Removed console.error to satisfy linter
    utterance.onerror = () => {
      setIsSpeaking(false);
    };

    window.speechSynthesis.speak(utterance);
  }, [voices]);

  return { speak, isSpeaking };
};