
import React from 'react';
import { Award, Users, Heart, ShieldCheck, Camera } from 'lucide-react';

const Nosotros: React.FC = () => {
  return (
    <div className="animate-in fade-in duration-500 pb-24">
      <header className="bg-gray-800 py-24 text-center">
        <h1 className="text-4xl md:text-6xl font-extrabold text-white mb-4">Nuestra Historia</h1>
        <p className="text-gray-400 max-w-2xl mx-auto px-4">Más de 15 años guiando aventuras y formando escaladores.</p>
      </header>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          <div className="relative group">
            <img 
              src="https://images.unsplash.com/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&q=80&w=800" 
              alt="Founders" 
              className="rounded-3xl shadow-xl grayscale hover:grayscale-0 transition-all duration-700"
            />
            <div className="absolute -top-4 -left-4 bg-orange-500 text-white p-6 rounded-2xl shadow-lg">
              <span className="text-3xl font-bold">18+</span>
              <p className="text-xs uppercase font-bold tracking-widest">Años de Exp.</p>
            </div>
          </div>
          <div>
            <h2 className="text-3xl font-bold text-gray-800 mb-6">Guías por vocación, aventureros por pasión</h2>
            <p className="text-gray-600 mb-6 leading-relaxed">
              Roca & Senda nació en 2006 de la mano de Dani y Nacho, dos guías titulados TD2 de Alta Montaña y Escalada que compartían un sueño: acercar la majestuosidad de las cumbres a todo aquel con ganas de aprender.
            </p>
            <p className="text-gray-600 mb-8 leading-relaxed">
              Lo que empezó como pequeñas salidas de fin de semana en la Sierra de Guadarrama se ha convertido en una agencia de referencia con expediciones internacionales y cursos técnicos de alto rendimiento.
            </p>
            
            <div className="grid grid-cols-2 gap-6">
              <div className="flex items-start space-x-3">
                <div className="bg-orange-100 p-2 rounded-lg text-orange-500">
                  <Award className="h-5 w-5" />
                </div>
                <div>
                  <h4 className="font-bold text-gray-800">Titulados</h4>
                  <p className="text-xs text-gray-500">Formación oficial AEGM</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="bg-gray-100 p-2 rounded-lg text-gray-800">
                  <Heart className="h-5 w-5" />
                </div>
                <div>
                  <h4 className="font-bold text-gray-800">Sostenibles</h4>
                  <p className="text-xs text-gray-500">Compromiso medioambiental</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* New Gallery Section: Momentos en la Cumbre */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-32">
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-orange-50 px-4 py-2 rounded-full text-orange-500 mb-4">
            <Camera className="h-4 w-4" />
            <span className="text-xs font-bold uppercase tracking-widest">Nuestro Día a Día</span>
          </div>
          <h2 className="text-4xl font-black text-gray-900">Momentos en la Cumbre</h2>
          <p className="text-gray-500 mt-4 max-w-xl mx-auto">Una mirada real a nuestras expediciones. Sin filtros, solo montaña y superación.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 h-auto md:h-[600px]">
          {/* Main vertical image */}
          <div className="md:col-span-2 md:row-span-2 relative group overflow-hidden rounded-[2.5rem] shadow-lg">
            <img 
              src="https://images.unsplash.com/photo-1533224860662-358d5c62b647?auto=format&fit=crop&q=80&w=800" 
              alt="Expedición Invierno" 
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-gray-900/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex flex-col justify-end p-8 text-white">
              <h4 className="font-bold text-xl">Amanecer en el Refugio</h4>
              <p className="text-sm text-gray-300">Dani preparando la ruta del día en el Pirineo.</p>
            </div>
          </div>

          {/* Horizontal top image */}
          <div className="md:col-span-2 relative group overflow-hidden rounded-[2.5rem] shadow-lg">
            <img 
              src="https://images.unsplash.com/photo-1522163182402-834f871fd851?auto=format&fit=crop&q=80&w=800" 
              alt="Escalada en Pared" 
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-orange-600/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex flex-col justify-end p-8 text-white">
              <h4 className="font-bold text-lg">Cursos de Iniciación</h4>
              <p className="text-xs text-orange-50">Nacho asegurando a un grupo de alumnos en granito.</p>
            </div>
          </div>

          {/* Small images */}
          <div className="relative group overflow-hidden rounded-[2.5rem] shadow-lg">
            <img 
              src="https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&q=80&w=800" 
              alt="Cima" 
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center p-4 text-center">
              <span className="text-white text-xs font-bold uppercase tracking-widest border border-white px-4 py-2 rounded-full">Cima Mulhacén</span>
            </div>
          </div>

          <div className="relative group overflow-hidden rounded-[2.5rem] shadow-lg">
            <img 
              src="https://images.unsplash.com/photo-1516733725897-1aa73b87c8e8?auto=format&fit=crop&q=80&w=800" 
              alt="Camino" 
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center p-4 text-center">
              <span className="text-white text-xs font-bold uppercase tracking-widest border border-white px-4 py-2 rounded-full">Valles Glaciares</span>
            </div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="bg-orange-500 py-24 mt-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-16">Nuestros Valores Fundamentales</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="bg-white/10 p-10 rounded-3xl backdrop-blur-md">
              <Users className="h-10 w-10 mx-auto mb-6" />
              <h3 className="text-xl font-bold mb-4">Cercanía</h3>
              <p className="text-orange-50 leading-relaxed">Grupos reducidos para garantizar una atención personalizada y un aprendizaje real.</p>
            </div>
            <div className="bg-white/10 p-10 rounded-3xl backdrop-blur-md">
              <ShieldCheck className="h-10 w-10 mx-auto mb-6" />
              <h3 className="text-xl font-bold mb-4">Seguridad</h3>
              <p className="text-orange-50 leading-relaxed">Protocolos de gestión de riesgos actualizados y supervisión constante en cada paso.</p>
            </div>
            <div className="bg-white/10 p-10 rounded-3xl backdrop-blur-md">
              <TreesIcon className="h-10 w-10 mx-auto mb-6" />
              <h3 className="text-xl font-bold mb-4">Respeto</h3>
              <p className="text-orange-50 leading-relaxed">No solo guiamos, enseñamos a amar y proteger las montañas que nos acogen.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// Icon component helper
const TreesIcon = ({ className }: { className?: string }) => (
  <svg className={className} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10 10v.01"/><path d="M14 10v.01"/><path d="M7 6a4 4 0 0 1 8 0 4 4 0 0 1 8 0v7a3 3 0 0 1-3 3h-15a3 3 0 0 1-3-3V6a4 4 0 0 1 8 0Z"/><path d="M12 19v3"/><path d="M9 22h6"/></svg>
);

export default Nosotros;
