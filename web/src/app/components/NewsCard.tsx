// components/NewsCard.tsx
import React from 'react';

interface NewsCardProps {
  title: string;
  description: string;
  date: string;
  imageUrl: string;
  newsUrl: string;
  score: number;
}

const NewsCard: React.FC<NewsCardProps> = ({
  title,
  description,
  date,
  imageUrl,
  newsUrl,
  score,
}) => {
  return (
    <div className="news-card">
      <h2>{title}</h2>
      <p>{description}</p>
      <p>{date}</p>
      <img src={imageUrl} alt={title} />
      <a href={newsUrl} target="_blank" rel="noopener noreferrer">
        Ver notícia completa
      </a>
      <p>Avaliação: {score}</p>
    </div>
  );
};

export default NewsCard;
