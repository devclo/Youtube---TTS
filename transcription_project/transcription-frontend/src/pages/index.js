import Head from 'next/head';
import { useState } from 'react';
import axios from 'axios';
import styles from '@/styles/Home.module.css'; // Make sure the path to your styles is correct




export default function Home() {
  const [videoUrl, setVideoUrl] = useState('');
  const [transcription, setTranscription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/transcribe/', { video_url: videoUrl });
      setTranscription(response.data);
    } catch (err) {
      console.error('There was an error!', err);
      setError('Failed to transcribe the video.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Head>
        <title>Video Transcriber</title>
        <meta name="description" content="Transcribe your videos easily" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Video Transcriber
        </h1>

        <div className={styles.transcriptionForm}>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              placeholder="Enter video URL"
              required
              className={styles.input}
            />
            <button type="submit" disabled={loading} className={styles.button}>
              {loading ? 'Transcribing...' : 'Transcribe'}
            </button>
          </form>

          {transcription && (
            <div className={styles.transcriptionResult}>
              <h2>Transcription Result:</h2>
              <p>{transcription.transcription_text}</p>
            </div>
          )}

          {error && <p className={styles.error}>{error}</p>}
        </div>
      </main>
    </div>
  );
}
