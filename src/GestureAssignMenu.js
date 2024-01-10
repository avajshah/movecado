import React, { useState } from 'react';
import './GestureAssignMenu.css';

const GestureAssignMenu = ({ gestureKeyMap, onGestureAssign, onDeleteGesture }) => {
  const [gesture, setGesture] = useState('');
  const [keypress, setKeypress] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onGestureAssign(gesture, keypress);
    setGesture('');
    setKeypress('');
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="assign-menu">
      <button className="assign-button" onClick={() => setIsModalOpen(true)}>
        Assign Gestures
      </button>
      {isModalOpen && (
        <div className={`modal ${isModalOpen ? 'show' : ''}`} onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <form onSubmit={handleSubmit}>
              <label>Gesture:</label>
              <input
                type="text"
                placeholder="Enter Gesture"
                value={gesture}
                onChange={(e) => setGesture(e.target.value)}
              />
              <label>Keypress:</label>
              <input
                type="text"
                placeholder="Assign Key"
                value={keypress}
                onChange={(e) => setKeypress(e.target.value)}
              />
              <button type="submit">Assign</button>
            </form>
            <div className="assigned-gestures">
              <h3>Assgined Gestures</h3>
              <ul>
                {Object.entries(gestureKeyMap).map(([assignedGesture, assignedKeypress]) => (
                    <li key={assignedGesture}>
                      {assignedGesture} - {assignedKeypress}{' '}
                      <button onClick={() => onDeleteGesture(assignedGesture)}>Delete</button>
                    </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestureAssignMenu;