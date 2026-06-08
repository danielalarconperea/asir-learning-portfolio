
import React, { useState } from 'react';
import { ROUTES } from '../constants';
import { Route } from '../types';
import { Clock, Euro, X, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';

const Servicios: React.FC = () => {
  const [filter, setFilter] = useState<'Todos' | 'Trekking' | 'Escalada'>('Todos');
  const [selectedRoute, setSelectedRoute] = useState<Route | null>(null);

  const filteredRoutes = filter === 'Todos' 
    ? ROUTES 
    : ROUTES.filter(r => r.category === filter);

  const closeModal = () => setSelectedRoute(null);

  return (
    <div className="animate-in fade-in duration-500 pb-24">
      <header className="bg-gray-800 py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">Catálogo de Aventuras</h1>
        <p className="text-gray-400 max-w-2xl mx-auto px-4">Encuentra el reto que mejor se adapte a tu nivel y pasión.</p>
      </header>

      {/* Filter Bar */}
      <div className="max-w-7xl mx-auto px-4 mt-12 mb-12 flex flex-wrap gap-4 justify-center">
        {['Todos', 'Trekking', 'Escalada'].map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat as any)}
            className={`px-8 py-2 rounded-full font-bold transition-all shadow-sm ${
              filter === cat ? 'bg-orange-500 text-white scale-105' : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-100'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Route Cards */}
      <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-10">
        {filteredRoutes.map((route) => (
          <div 
            key={route.id} 
            onClick={() => setSelectedRoute(route)}
            className="bg-white rounded-3xl overflow-hidden shadow-lg border border-gray-100 hover:shadow-2xl transition-all group cursor-pointer"
          >
            <div className="relative h-64 overflow-hidden bg-gray-200">
              <img 
                src={route.image} 
                alt={route.title} 
                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1516733725897-1aa73b87c8e8?auto=format&fit=crop&q=80&w=800';
                }}
              />
              <div className="absolute top-4 left-4 bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">
                {route.category}
              </div>
              <div className="absolute bottom-4 right-4 bg-white/90 backdrop-blur-sm text-gray-800 text-sm font-bold px-4 py-2 rounded-xl shadow-lg">
                {route.difficulty}
              </div>
            </div>
            <div className="p-8">
              <h3 className="text-2xl font-bold text-gray-800 mb-4 group-hover:text-orange-500 transition-colors">{route.title}</h3>
              <p className="text-gray-600 mb-6 line-clamp-2 leading-relaxed">{route.description}</p>
              
              <div className="flex items-center justify-between pt-6 border-t border-gray-100">
                <div className="flex space-x-6 text-sm text-gray-500 font-medium">
                  <div className="flex items-center">
                    <Clock className="h-4 w-4 mr-2 text-orange-500" />
                    {route.duration}
                  </div>
                  <div className="flex items-center">
                    <Euro className="h-4 w-4 mr-1 text-orange-500" />
                    {route.price}
                  </div>
                </div>
                <button className="text-orange-500 font-bold hover:text-gray-800 transition-colors uppercase text-sm tracking-widest">
                  Ver Info
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Detail Modal */}
      {selectedRoute && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-gray-900/80 backdrop-blur-md animate-in fade-in duration-300">
          <div 
            className="bg-white w-full max-w-5xl max-h-[90vh] overflow-y-auto rounded-[2.5rem] shadow-2xl relative animate-in zoom-in-95 duration-300"
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              onClick={closeModal}
              className="absolute top-6 right-6 z-10 bg-white/20 hover:bg-orange-500 hover:text-white transition-all p-3 rounded-full text-gray-800 backdrop-blur-md"
            >
              <X className="h-6 w-6" />
            </button>

            <div className="flex flex-col lg:flex-row">
              {/* Image Side */}
              <div className="lg:w-1/2 h-72 lg:h-auto sticky top-0">
                <img 
                  src={selectedRoute.image} 
                  alt={selectedRoute.title}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Content Side */}
              <div className="lg:w-1/2 p-8 lg:p-12">
                <div className="flex items-center space-x-3 mb-4">
                  <span className="bg-orange-100 text-orange-500 text-xs font-black px-3 py-1 rounded-full uppercase tracking-widest">
                    {selectedRoute.category}
                  </span>
                  <span className="bg-gray-100 text-gray-600 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-widest">
                    Nivel {selectedRoute.difficulty}
                  </span>
                </div>

                <h2 className="text-4xl font-extrabold text-gray-900 mb-6 leading-tight">
                  {selectedRoute.title}
                </h2>

                <p className="text-lg text-gray-600 mb-8 leading-relaxed">
                  {selectedRoute.description}
                </p>

                <div className="grid grid-cols-2 gap-6 mb-10">
                  <div className="bg-gray-50 p-4 rounded-2xl flex items-center space-x-4">
                    <div className="bg-white p-3 rounded-xl shadow-sm text-orange-500">
                      <Clock className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-xs text-gray-400 font-bold uppercase tracking-widest">Duración</p>
                      <p className="font-bold text-gray-800">{selectedRoute.duration}</p>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-2xl flex items-center space-x-4">
                    <div className="bg-white p-3 rounded-xl shadow-sm text-orange-500">
                      <Euro className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-xs text-gray-400 font-bold uppercase tracking-widest">Desde</p>
                      <p className="font-bold text-gray-800">{selectedRoute.price}</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-8">
                  <div>
                    <h4 className="text-sm font-black text-gray-900 uppercase tracking-widest mb-4 flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-green-500" />
                      Lo que incluye
                    </h4>
                    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {['Guía Titulado TD2', 'Seguro de Accidentes', 'Material Colectivo', 'Gestión de Refugios', 'Reportaje Fotográfico'].map((item, i) => (
                        <li key={i} className="text-sm text-gray-600 flex items-center">
                          <span className="w-1.5 h-1.5 bg-orange-400 rounded-full mr-2"></span>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="text-sm font-black text-gray-900 uppercase tracking-widest mb-4 flex items-center">
                      <AlertTriangle className="h-4 w-4 mr-2 text-orange-500" />
                      Requisitos
                    </h4>
                    <p className="text-sm text-gray-500">
                      {selectedRoute.difficulty === 'Difícil' || selectedRoute.difficulty === 'Experto' 
                        ? 'Es necesaria una condición física excelente y experiencia previa en terrenos técnicos de montaña.' 
                        : 'No se requiere experiencia técnica previa, solo una condición física saludable y muchas ganas de aventura.'}
                    </p>
                  </div>
                </div>

                <div className="mt-12">
                  <button className="w-full bg-orange-500 hover:bg-gray-800 text-white font-black py-5 rounded-2xl transition-all shadow-xl hover:shadow-orange-500/20 flex items-center justify-center group uppercase tracking-widest">
                    Reservar plaza ahora
                    <ArrowRight className="ml-3 h-5 w-5 group-hover:translate-x-2 transition-transform" />
                  </button>
                  <p className="text-center text-[10px] text-gray-400 mt-4 uppercase font-bold tracking-widest">
                    Plazas limitadas por grupo (máx 6 personas)
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Servicios;
