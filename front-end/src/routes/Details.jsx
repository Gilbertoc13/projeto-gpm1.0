import React from 'react';
import { useParams } from 'react-router-dom';

function Details() {
  const { tipo, id } = useParams();

  console.log(tipo, id);

  return (
    <div>
      <h2>Detalhes do {tipo} {id}</h2>
    </div>
  );
}

export default Details;
