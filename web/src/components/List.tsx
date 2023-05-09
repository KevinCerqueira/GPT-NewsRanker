// src/components/List.tsx
import React, { useState, useEffect } from 'react';
import ListItem from './ListItem';
import axios from 'axios';

interface Item {
  title: string;
  description: string;
  date: string;
  score: number;
  image: string;
  link: string;
}

const List: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);

  useEffect(() => {
    axios.get('https://api-kevin-exa844.onrender.com/news')
      .then((response) => {
        setItems(response.data);
		console.log(response.data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div className="list">
      {items.map((item, index) => (
        <ListItem
          key={index}
          title={item.title}
          description={item.description}
          date={item.date}
          score={item.score}
          image={item.image}
          link={item.link}
        />
      ))}
    </div>
  );
};

export default List;
