import React from "react";

const SportBot = ({ name, number, imageUrl, stats, traits }) => {
  return (
    <div className="card">
      <img src={imageUrl} alt={`SportBot #${number}`} className="card-img-top" />
      <div className="card-body">
        <h5 className="card-title">{name}</h5>
        <ul className="list-group list-group-flush">
          {traits && (
            <>
                <li className="list-group-item">Sport: {traits.sport}</li>
                <li className="list-group-item">Sportshares: {stats.sportshares}</li>
                <li className="list-group-item">Freebet: {stats.freebet}</li>
                <li className="list-group-item">Comboboost: {stats.comboboost}</li>
            </>
          )}
        </ul>
      </div>
    </div>
  );
};

export default SportBot;
