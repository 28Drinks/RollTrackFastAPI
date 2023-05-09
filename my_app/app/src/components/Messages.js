import React from "react";

const FlashMessage = ({ message, type }) => {
  return (
    <div className={`notification is-${type}`}>
      <button className="delete"></button>
      {message}
    </div>
  );
};

export default FlashMessage;