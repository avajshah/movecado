import React from 'react';
import Webcam from 'react-webcam';
import './CameraComponent.css';

const CameraComponent = () => {
    return (
        <div className = 'camera-container'>
            <Webcam className = 'webcam' mirrored = {true}/>
        </div>
    );
};

export default CameraComponent