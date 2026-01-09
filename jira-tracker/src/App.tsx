/**
 * Componente principal de la aplicación
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { ProjectWorkspace } from './pages/ProjectWorkspace';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/project/:projectKey" element={<ProjectWorkspace />} />
      </Routes>
    </Router>
  );
}

export default App;
