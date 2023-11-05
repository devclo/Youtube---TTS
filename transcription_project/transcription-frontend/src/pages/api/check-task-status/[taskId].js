// pages/api/check-task-status/[taskId].js

import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const taskId = req.query.taskId;
    try {
      // Make a GET request to your Django backend to check the task status
      // Replace YOUR_DJANGO_BACKEND_HOST with your actual Django backend host address
      const response = await axios.get(`http://localhost:8000/api/transcribe/${taskId}`);
      
      // Send the response back to the client
      res.status(200).json(response.data);
    } catch (error) {
      console.error('Error checking transcription task status:', error);
      res.status(error.response?.status || 500).json({ message: 'Error checking transcription task status' });
    }
  } else {
    // If the request method is not GET, return a 405 Method Not Allowed error
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
