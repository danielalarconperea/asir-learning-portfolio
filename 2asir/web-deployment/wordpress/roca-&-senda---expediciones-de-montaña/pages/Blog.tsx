
import React from 'react';
import { BLOG_POSTS } from '../constants';
import { Calendar, User, ArrowRight } from 'lucide-react';

const Blog: React.FC = () => {
  return (
    <div className="animate-in fade-in duration-500 pb-24">
      <header className="bg-gray-800 py-24 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">Blog de Montaña</h1>
        <p className="text-gray-400 max-w-2xl mx-auto px-4">Consejos, guías técnicas y crónicas de nuestras últimas expediciones.</p>
      </header>

      <section className="max-w-7xl mx-auto px-4 mt-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          {BLOG_POSTS.map((post) => (
            <article key={post.id} className="group cursor-pointer">
              <div className="relative h-[400px] overflow-hidden rounded-[2.5rem] mb-8 shadow-xl">
                <img 
                  src={post.image} 
                  alt={post.title} 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-1000"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-gray-900/60 to-transparent opacity-60"></div>
                <div className="absolute bottom-6 left-6 flex space-x-4">
                  <div className="bg-white/90 backdrop-blur-sm px-4 py-2 rounded-xl text-xs font-bold text-gray-800 flex items-center shadow-lg">
                    <Calendar className="h-3 w-3 mr-2 text-orange-500" />
                    {post.date}
                  </div>
                  <div className="bg-orange-500 px-4 py-2 rounded-xl text-xs font-bold text-white flex items-center shadow-lg">
                    <User className="h-3 w-3 mr-2" />
                    Guía Roca & Senda
                  </div>
                </div>
              </div>
              <h2 className="text-3xl font-extrabold text-gray-800 mb-4 group-hover:text-orange-500 transition-colors leading-tight">
                {post.title}
              </h2>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                {post.excerpt}
              </p>
              <button className="inline-flex items-center font-bold text-orange-500 uppercase tracking-widest text-sm group-hover:underline decoration-2 underline-offset-8">
                Leer más <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-2 transition-transform" />
              </button>
            </article>
          ))}
        </div>
      </section>

      {/* Newsletter */}
      <section className="max-w-4xl mx-auto px-4 mt-32 bg-orange-50 p-16 rounded-[3rem] text-center border border-orange-100">
        <h3 className="text-3xl font-bold text-gray-800 mb-4">No te pierdas ninguna expedición</h3>
        <p className="text-gray-600 mb-8">Suscríbete a nuestra newsletter para recibir consejos técnicos y ofertas exclusivas.</p>
        <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
          <input 
            type="email" 
            placeholder="Tu email"
            className="flex-1 px-6 py-4 rounded-2xl bg-white border border-orange-200 outline-none focus:ring-2 focus:ring-orange-500 transition-all"
          />
          <button className="bg-gray-800 text-white px-8 py-4 rounded-2xl font-bold hover:bg-orange-500 transition-all">
            Unirme
          </button>
        </div>
      </section>
    </div>
  );
};

export default Blog;
