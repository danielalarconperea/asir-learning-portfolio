
import React, { useState } from 'react';
import { Mail, Phone, MapPin, Send, CheckCircle2 } from 'lucide-react';

const Contacto: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    // Simulating WPForms behavior
    setTimeout(() => setSubmitted(false), 5000);
  };

  return (
    <div className="animate-in fade-in duration-500">
      <header className="bg-gray-800 py-24 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">Hablemos de tu reto</h1>
        <p className="text-gray-400 max-w-2xl mx-auto px-4">Nuestro equipo de guías está listo para asesorarte.</p>
      </header>

      <section className="max-w-7xl mx-auto px-4 py-24">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-20">
          {/* Contact Info */}
          <div>
            <h2 className="text-3xl font-bold text-gray-800 mb-8">Información de Contacto</h2>
            <p className="text-gray-600 mb-12 leading-relaxed">
              Estamos ubicados en las faldas de la Sierra de Madrid, pero operamos en todo el territorio nacional. Si prefieres hablar directamente con un guía, no dudes en llamarnos.
            </p>
            
            <div className="space-y-8">
              <div className="flex items-start space-x-6">
                <div className="bg-orange-500 p-4 rounded-2xl text-white shadow-lg">
                  <MapPin className="h-6 w-6" />
                </div>
                <div>
                  <h4 className="font-bold text-gray-800 text-lg">Nuestra Base</h4>
                  <p className="text-gray-600">Puerto de Navacerrada, Madrid, España</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-6">
                <div className="bg-orange-500 p-4 rounded-2xl text-white shadow-lg">
                  <Phone className="h-6 w-6" />
                </div>
                <div>
                  <h4 className="font-bold text-gray-800 text-lg">Teléfono</h4>
                  <p className="text-gray-600">+34 600 000 000</p>
                </div>
              </div>

              <div className="flex items-start space-x-6">
                <div className="bg-orange-500 p-4 rounded-2xl text-white shadow-lg">
                  <Mail className="h-6 w-6" />
                </div>
                <div>
                  <h4 className="font-bold text-gray-800 text-lg">Email</h4>
                  <p className="text-gray-600">info@rocaysenda.com</p>
                </div>
              </div>
            </div>

            {/* Simulated Google Map */}
            <div className="mt-16 bg-gray-100 rounded-[2rem] h-80 overflow-hidden relative shadow-inner border border-gray-200">
              <div className="absolute inset-0 flex items-center justify-center bg-cover bg-center" style={{ backgroundImage: 'url(https://images.unsplash.com/photo-1544198365-f5d60b6d8190?auto=format&fit=crop&q=80&w=800)' }}>
                <div className="absolute inset-0 bg-white/20 backdrop-blur-[2px]"></div>
                <div className="z-10 bg-white p-6 rounded-2xl shadow-2xl flex flex-col items-center">
                  <MapPin className="h-8 w-8 text-orange-500 mb-2" />
                  <span className="font-bold text-gray-800">Parque Nacional de Guadarrama</span>
                  <span className="text-xs text-gray-500">Zona de entrenamiento Roca & Senda</span>
                  <a href="https://maps.google.com" target="_blank" rel="noreferrer" className="mt-4 text-xs font-bold text-orange-500 hover:underline uppercase tracking-widest">Ver en Google Maps</a>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form (Simulating WPForms) */}
          <div className="bg-white rounded-[3rem] p-10 shadow-2xl border border-gray-50">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Envíanos un mensaje</h3>
            {submitted ? (
              <div className="bg-green-50 text-green-700 p-8 rounded-2xl border border-green-100 flex flex-col items-center text-center animate-in zoom-in duration-300">
                <CheckCircle2 className="h-12 w-12 mb-4" />
                <h4 className="font-bold text-lg mb-2">¡Mensaje Enviado!</h4>
                <p>Gracias por contactar con Roca & Senda. Un guía se pondrá en contacto contigo en menos de 24 horas.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">Nombre</label>
                    <input 
                      required 
                      type="text" 
                      placeholder="Tu nombre completo"
                      className="w-full px-4 py-4 rounded-xl bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">Email</label>
                    <input 
                      required 
                      type="email" 
                      placeholder="hola@ejemplo.com"
                      className="w-full px-4 py-4 rounded-xl bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">Actividad de Interés</label>
                  <select className="w-full px-4 py-4 rounded-xl bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none appearance-none">
                    <option>Trekking de varios días</option>
                    <option>Curso de Escalada Iniciación</option>
                    <option>Curso de Escalada Perfeccionamiento</option>
                    <option>Ascensiones a medida</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">Mensaje</label>
                  <textarea 
                    rows={4}
                    placeholder="Cuéntanos tu experiencia previa y qué buscas..."
                    className="w-full px-4 py-4 rounded-xl bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none resize-none"
                  ></textarea>
                </div>
                <button 
                  type="submit" 
                  className="w-full bg-orange-500 text-white font-bold py-4 rounded-xl shadow-lg hover:bg-gray-800 transition-all flex items-center justify-center group"
                >
                  Enviar Formulario
                  <Send className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </button>
                <p className="text-[10px] text-gray-400 text-center uppercase tracking-widest font-bold">
                  Este formulario cumple con el RGPD y los protocolos de Roca & Senda.
                </p>
              </form>
            )}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contacto;
