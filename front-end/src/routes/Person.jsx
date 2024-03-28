import React from 'react';
import { useParams } from 'react-router-dom';

function Person() {
  const { id } = useParams();

  console.log(id);

  return (
    <div>
      <h2>Pessoa {id}</h2>
    </div>
  );
}

export default Person;
