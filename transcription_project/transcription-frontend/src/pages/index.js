import axios from 'axios';
import { useState } from 'react';

export default function Home() {
  const [videoURL, setVideoURL] = useState('');
  const [processing, setProcessing] = useState(false);
  const [videoInfo, setVideoInfo] = useState(null);
  const [taskId, setTaskId] = useState(null);

  // Function to poll for the result of the transcription
  const pollForTranscription = async (taskId) => {
    try {
      // Polling every 5 seconds (5000 milliseconds)
      const intervalId = setInterval(async () => {
        const response = await axios.get(`/api/check-task-status/${taskId}`);
        const { status, result } = response.data;

        if (status === 'SUCCESS') {
          clearInterval(intervalId);
          setVideoInfo({ ...videoInfo, transcription: result });
          setProcessing(false);
        } else if (status === 'FAILURE') {
          clearInterval(intervalId);
          setProcessing(false);
          // You should add proper error handling here
          console.error('Error transcribing video');
        }
        // If the status is 'PENDING' or 'STARTED', we do nothing and keep polling
      }, 5000);
    } catch (error) {
      clearInterval(intervalId);
      setProcessing(false);
      console.error('Error polling for transcription:', error);
    }
  };

  const handleTranscribe = async () => {
    setProcessing(true);
    try {
      // Start the transcription task
      const response = await axios.post('/api/transcribe-video', { video_url: videoURL });
      const { task_id } = response.data;
      setTaskId(task_id);
      
      // Poll for the result of the transcription
      pollForTranscription(task_id);
    } catch (error) {
      console.error('Error starting transcription task:', error);
      setProcessing(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={videoURL}
        onChange={(e) => setVideoURL(e.target.value)}
        placeholder="Enter YouTube Video URL"
      />
      <button onClick={handleTranscribe} disabled={processing}>
        {processing ? 'Processing...' : 'Transcribe Video'}
      </button>

      {videoInfo && (
        <div>
          {/* Display video information and buttons to download and show transcription */}
          <p>Title: {videoInfo.title}</p>
          {/* Embed the YouTube video if videoId is available */}
          {videoInfo.videoId && (
            <iframe
              width="560"
              height="315"
              src={`https://www.youtube.com/embed/${videoInfo.videoId}`} 
              title="YouTube video player"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          )}
          
          {/* Assuming `videoInfo` has a property `transcriptionUrl` for downloading the transcription */}
          {videoInfo.transcriptionUrl && (
            <a href={videoInfo.transcriptionUrl} download="transcription.txt">
              Download Transcription
            </a>
          )}

          {/* Assuming `videoInfo` has a property `transcription` which contains the transcription text */}
          {videoInfo.transcription && (
            <div>
              <h3>Transcription Preview:</h3>
              <p>{videoInfo.transcription}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

