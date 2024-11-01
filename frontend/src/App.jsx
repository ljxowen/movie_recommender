import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import SignIn from './pages/SignIn';
import MovieDetail from './pages/MovieDetail';

import { loginRequest } from './api/loginService';
import { OpenAPI } from './client/core/OpenAPI';

import {setToken, getToken} from './utils/loginToken'
import AddMovie from './pages/AddMovie';

import './App.css';

function App() {

  // 登录并获取 token
  useEffect(() => {
    const loginService = async () => {
      const response = await loginRequest('liujingxuanowen@gmail.com', '0427');
      //存储token到会话存储，但是目前没意义。。。。
      setToken(response.access_token);
      const token = getToken();
      OpenAPI.TOKEN = token; // 更新 token
    }

    loginService();
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/AddMovie" element={<AddMovie />} />
        <Route path="/SignIn" element={<SignIn />} />
        <Route path="/MovieDetail/:id" element={<MovieDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
