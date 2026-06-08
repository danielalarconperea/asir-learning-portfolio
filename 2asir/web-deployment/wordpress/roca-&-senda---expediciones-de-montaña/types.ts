
export interface Route {
  id: string;
  title: string;
  category: 'Trekking' | 'Escalada';
  difficulty: 'Fácil' | 'Moderado' | 'Difícil' | 'Experto';
  price: string;
  description: string;
  image: string;
  duration: string;
}

export interface BlogPost {
  id: number;
  title: string;
  date: string;
  excerpt: string;
  content: string;
  image: string;
}
