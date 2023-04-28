// components/NewsList.tsx
import React from 'react';
import NewsCard from './NewsCard';

interface News {
  title: string;
  description: string;
  date: string;
  imageUrl: string;
  newsUrl: string;
  score: number;
}

interface NewsListProps {
  news: News[];
}

const NewsList: React.FC<NewsListProps> = ({ news }) => {
  return (
    <div className="news-list">
      {news.map((newsItem, index) => (
        <NewsCard key={index} {...newsItem} />
      ))}
    </div>
  );
};

export default NewsList;
