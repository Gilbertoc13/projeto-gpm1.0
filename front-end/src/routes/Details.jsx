import '../index.css';

import React from 'react';

const Detalhes = ({ match }) => {
  const { tipo, id } = match.params;

  return (
    <div>
      <h2>Detalhes do {tipo} com ID {id}</h2>
    </div>
  );
};

export default Detalhes;
