import React, { useState } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [characters] = useState(['Char1', 'Char2']);  // Up to 8, with icons
  const [images, setImages] = useState([]);  // For uploaded pics

  const handleSend = () => {
    if (input) {
      setMessages([...messages, { text: input, sender: 'User' }]);
      setInput('');
      // TODO: Call backend for AI responses from characters
    }
  };

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setImages([...images, url]);
      setMessages([...messages, { image: url, sender: 'User' }]);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Top Panel: Settings, logout, export, errors */}
      <header className="bg-gray-800 p-4 flex justify-between text-white">
        <div>Amora Chat</div>
        <div>
          <button>Settings</button>
          <button>Logout</button>
          <button>Export Chat</button>
          <span className="ml-4 text-red-500">No errors</span>
        </div>
      </header>
      <div className="flex flex-1">
        {/* Left Panel: Chat name, characters with icons */}
        <aside className="w-1/4 bg-gray-700 p-4 text-white">
          <h2>Current Chat: NSFW Group</h2>
          <ul>
            {characters.map((char, i) => (
              <li key={i} className="flex items-center">
                <img src="/path/to/icon.png" alt={char} className="w-8 h-8 mr-2" /> {char}
              </li>
            ))}
          </ul>
        </aside>
        {/* Central Panel: Chat display with text/images */}
        <main className="flex-1 p-4 overflow-y-auto">
          {messages.map((msg, i) => (
            <div key={i} className="mb-2">
              {msg.text && <p>{msg.sender}: {msg.text}</p>}
              {msg.image && <img src={msg.image} alt="Uploaded" className="max-w-xs" />}
            </div>
          ))}
        </main>
      </div>
      {/* Bottom Panel: Input, send, upload */}
      <footer className="bg-gray-800 p-4 flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 p-2 mr-2"
          placeholder="Type message..."
        />
        <button onClick={handleSend} className="bg-blue-500 p-2 mr-2">Send</button>
        <input type="file" accept="image/*" onChange={handleUpload} className="hidden" id="upload" />
        <label htmlFor="upload" className="bg-green-500 p-2 cursor-pointer">Upload Image</label>
      </footer>
    </div>
  );
}

export default App;
