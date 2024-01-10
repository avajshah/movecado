import logo from './logo.svg';
import './App.css';
import GestureAssignMenu from './GestureAssignMenu';
import React, { useState } from 'react';
import Webcam from "react-webcam";

import CameraComponent from './CameraComponent';

const App = () => {
  const [gestureKeyMap, setGestureKeyMap] = useState({});
  const handleGestureAssign = (gesture, keypress) => {
    setGestureKeyMap((prevMap) => ({...prevMap, [gesture]:keypress }));
  };

  return (
    <div className = 'app-container'>
      <div className = 'taskbar'>
        <h1>Movecado</h1>
        <GestureAssignMenu 
        gestureKeyMap = {gestureKeyMap}
        onGestureAssign = {handleGestureAssign}
        onDeleteGesture = {(gesture) => {
            const updatedKeyMap = {...gestureKeyMap};
            delete updatedKeyMap[gesture];
            setGestureKeyMap(updatedKeyMap);
          }}
        />
        </div>
        <div className = 'camera-container'>
         <CameraComponent/>
        </div>
      
    </div>
  )
}

export default App;
