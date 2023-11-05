// pages/api/transcribe-video.js

export default function handler(req, res) {
  if (req.method === 'POST') {
    // Your API logic here
    res.status(200).json({ message: 'Video transcribed successfully!' });
  } else {
    // Handle any other HTTP method
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
