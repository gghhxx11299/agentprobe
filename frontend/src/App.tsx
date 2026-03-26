import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Configure from './pages/Configure';
import Dashboard from './pages/Dashboard';
import TargetPage from './pages/TargetPage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/configure" element={<Configure />} />
        <Route path="/session/:session_id" element={<Dashboard />} />
        <Route path="/test/:session_id" element={<TargetPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
