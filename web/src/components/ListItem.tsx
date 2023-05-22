// src/components/ListItem.tsx
import React from 'react';

interface ListItemProps {
  title: string;
  description: string;
  date: string;
  score: number;
  image: string;
  link: string;
}

const ListItem: React.FC<ListItemProps> = ({ title, description, date, score, image, link }) => {
  return (
    <div className="list-item">
      <h3>{title}</h3>
      <p>{description}</p>
      <p>Data: {date}</p>
      <p>Avaliação: {score}</p>
      <img src={image} alt={title} />
      <a href={link} target="_blank" rel="noopener noreferrer">
        Visite o site
      </a>
    </div>
  );
};

export default ListItem;
