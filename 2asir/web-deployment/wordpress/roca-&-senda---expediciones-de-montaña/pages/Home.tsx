
import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Mountain, Shield, Trees } from 'lucide-react';

const Home: React.FC = () => {
  return (
    <div className="animate-in fade-in duration-700">
      {/* Hero Section */}
      <section className="relative h-[85vh] flex items-center overflow-hidden">
        <div className="absolute inset-0">
          <img 
            src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=1920" 
            alt="Mountains" 
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gray-900/40"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-white">
          <div className="max-w-2xl">
            <h1 className="text-5xl md:text-7xl font-extrabold leading-tight mb-6">
              Tu próxima aventura comienza en la <span className="text-orange-500">cima</span>.
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-gray-100 font-light">
              Expediciones guiadas de trekking y cursos de escalada técnica. Vive la montaña con seguridad.
            </p>
            <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
              <Link to="/servicios" className="bg-orange-500 hover:bg-white hover:text-orange-500 text-white px-8 py-4 rounded-full font-bold text-lg transition-all flex items-center justify-center group shadow-xl">
                Ver Rutas
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link to="/contacto" className="bg-white/10 backdrop-blur-md border border-white/20 hover:bg-white/20 text-white px-8 py-4 rounded-full font-bold text-lg transition-all text-center">
                Contactar Ahora
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats/Highlights */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
            <div className="p-8 rounded-3xl hover:bg-orange-50 transition-colors group">
              <div className="w-16 h-16 bg-orange-100 text-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-orange-500 group-hover:text-white transition-all">
                <Shield className="h-8 w-8" />
              </div>
              <h3 className="text-xl font-bold mb-4 text-gray-800">Seguridad Total</h3>
              <p className="text-gray-600 leading-relaxed">
                Guías de alta montaña titulados y material homologado para todas nuestras actividades.
              </p>
            </div>
            <div className="p-8 rounded-3xl hover:bg-gray-50 transition-colors group">
              <div className="w-16 h-16 bg-gray-100 text-gray-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-gray-800 group-hover:text-white transition-all">
                <Mountain className="h-8 w-8" />
              </div>
              <h3 className="text-xl font-bold mb-4 text-gray-800">Todos los Niveles</h3>
              <p className="text-gray-600 leading-relaxed">
                Desde rutas familiares de senderismo hasta ascensiones técnicas y cursos de escalada.
              </p>
            </div>
            <div className="p-8 rounded-3xl hover:bg-orange-50 transition-colors group">
              <div className="w-16 h-16 bg-orange-100 text-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-orange-500 group-hover:text-white transition-all">
                <Trees className="h-8 w-8" />
              </div>
              <h3 className="text-xl font-bold mb-4 text-gray-800">Ecoturismo</h3>
              <p className="text-gray-600 leading-relaxed">
                Respetamos el entorno natural aplicando políticas de "no dejar rastro" en cada expedición.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Service */}
      <section className="py-24 bg-gray-50 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center gap-16">
            <div className="flex-1">
              <span className="text-orange-500 font-bold tracking-widest uppercase text-sm">Destacado</span>
              <h2 className="text-4xl md:text-5xl font-extrabold text-gray-800 mt-4 mb-6">Travesía de los Pirineos</h2>
              <p className="text-lg text-gray-600 mb-8 leading-relaxed">
                Nuestra expedición más popular. 5 días cruzando los paisajes más salvajes del Pirineo Aragonés. Refugios de montaña, lagos glaciares y la mejor compañía.
              </p>
              <div className="space-y-4 mb-8">
                <div className="flex items-center text-gray-700">
                  <div className="w-6 h-6 rounded-full bg-orange-500/10 text-orange-500 flex items-center justify-center mr-3 font-bold text-xs">✓</div>
                  Guías locales expertos
                </div>
                <div className="flex items-center text-gray-700">
                  <div className="w-6 h-6 rounded-full bg-orange-500/10 text-orange-500 flex items-center justify-center mr-3 font-bold text-xs">✓</div>
                  Material colectivo incluido
                </div>
                <div className="flex items-center text-gray-700">
                  <div className="w-6 h-6 rounded-full bg-orange-500/10 text-orange-500 flex items-center justify-center mr-3 font-bold text-xs">✓</div>
                  Seguro de accidentes
                </div>
              </div>
              <Link to="/servicios" className="inline-flex items-center font-bold text-orange-500 hover:text-gray-800 transition-colors">
                Ver detalles del catálogo <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </div>
            <div className="flex-1 relative">
              <img 
                src="https://images.unsplash.com/photo-1551632811-561732d1e306?auto=format&fit=crop&q=80&w=800" 
                alt="Trekking" 
                className="rounded-3xl shadow-2xl z-10 relative"
              />
              <div className="absolute -bottom-6 -right-6 w-64 h-64 bg-orange-500/10 rounded-full blur-3xl -z-0"></div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
