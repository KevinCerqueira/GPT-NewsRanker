// pages/index.tsx
import React from 'react';
import NewsList from './components/NewsList';
import { GetServerSideProps } from 'next';

interface News {
  title: string;
  description: string;
  date: string;
  imageUrl: string;
  newsUrl: string;
  score: number;
}

interface HomePageProps {
  news: News[];
}

const Home: React.FC<HomePageProps> = ({ news }) => {
  return (
    <div>
      <h1>Notícias</h1>
      <NewsList news={news} />
    </div>
  );
};

export const getServerSideProps: GetServerSideProps = async () => {
  try {
    const response = await fetch('http://192.168.1.100:5000/news');
    const news = await response.json();

    return {
      props: { news },
    };
  } catch (error) {
    console.error('Erro ao buscar notícias:', error);

    return {
      props: { news: [] },
    };
  }
};

export default Home;
