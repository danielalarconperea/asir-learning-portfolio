import { Route, BlogPost } from './types';

export const COLORS = {
  primary: '#F97316', // Orange
  secondary: '#374151', // Charcoal Gray
};

export const ROUTES: Route[] = [
  {
    id: '1',
    title: 'Travesía de los Pirineos',
    category: 'Trekking',
    difficulty: 'Difícil',
    price: '450€',
    duration: '5 días',
    description: 'Una expedición épica cruzando los valles más emblemáticos del Pirineo Aragonés. Incluye guía titulado y refugios.',
    image: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=800'
  },
  {
    id: '2',
    title: 'Ascensión al Mulhacén',
    category: 'Trekking',
    difficulty: 'Moderado',
    price: '180€',
    duration: '2 días',
    description: 'Corona el techo de la península en una ruta de senderismo de alta montaña con vistas espectaculares.',
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&q=80&w=800'
  },
  {
    id: '3',
    title: 'Iniciación a la Escalada en Roca',
    category: 'Escalada',
    difficulty: 'Fácil',
    price: '90€',
    duration: '1 día',
    description: 'Aprende las técnicas básicas de seguridad, nudos y progresión en paredes naturales de granito.',
    image: 'https://images.unsplash.com/photo-1522163182402-834f871fd851?auto=format&fit=crop&q=80&w=800'
  },
  {
    id: '4',
    title: 'Perfeccionamiento: Vía Larga',
    category: 'Escalada',
    difficulty: 'Experto',
    price: '220€',
    duration: '2 días',
    description: 'Para escaladores con experiencia que buscan dar el salto a las grandes paredes de varios largos.',
    image: 'https://images.unsplash.com/photo-1516592673814-189c5d27ff43?auto=format&fit=crop&q=80&w=800'
  }
];

export const BLOG_POSTS: BlogPost[] = [
  {
    id: 1,
    title: 'Equipo básico para tu primera escalada en roca',
    date: '15 de Mayo, 2024',
    excerpt: '¿Vas a empezar a escalar? Aquí tienes la lista definitiva del material imprescindible.',
    content: 'La escalada es un deporte apasionante que requiere un equipo técnico específico para garantizar la seguridad...',
    image: 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80&w=800'
  },
  {
    id: 2,
    title: 'Cómo prepararse físicamente para un trekking de 5 días',
    date: '22 de Junio, 2024',
    excerpt: 'Entrenamiento de resistencia y consejos de nutrición para disfrutar de la alta montaña.',
    content: 'Una travesía de varios días exige una buena base aeróbica y fuerza en el tren inferior...',
    image: 'https://images.unsplash.com/photo-1501555088652-021faa106b9b?auto=format&fit=crop&q=80&w=800'
  }
];