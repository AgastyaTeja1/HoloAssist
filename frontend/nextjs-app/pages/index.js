import { useEffect, useRef } from 'react';

export default function Home() {
  const videoRef = useRef();
  const canvasRef = useRef();

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.binaryType = 'arraybuffer';
    ws.onmessage = ({ data }) => {
      const msg = JSON.parse(data);
      if (msg.overlay) {
        const ctx = canvasRef.current.getContext('2d');
        ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
        ctx.font = '18px Arial';
        msg.overlay.split('\n').forEach((line, i) => {
          ctx.fillText(line, 10, 30 + i * 24);
        });
      }
    };

    async function start() {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      videoRef.current.srcObject = stream;

      const recorder = new MediaRecorder(stream, { mimeType: 'video/webm; codecs=vp8,opus' });
      recorder.ondataavailable = e => ws.send(e.data);
      recorder.start(200);
    }

    start();
    return () => ws.close();
  }, []);

  return (
    <div style={{ position: 'relative' }}>
      <video ref={videoRef} autoPlay muted playsInline width="640" height="480" />
      <canvas ref={canvasRef} width="640" height="480"
              style={{ position: 'absolute', top: 0, left: 0 }} />
    </div>
  );
}
