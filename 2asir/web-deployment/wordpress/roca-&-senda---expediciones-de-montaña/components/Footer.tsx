
import React from 'react';
import { Mountain, Instagram, Facebook, Twitter, Mail, Phone } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-12">
        <div className="space-y-4">
          <div className="flex items-center space-x-2">
            <Mountain className="h-8 w-8 text-orange-500" />
            <span className="text-2xl font-bold">ROCA & SENDA</span>
          </div>
          <p className="text-gray-400 text-sm leading-relaxed">
            Tu agencia de confianza para expediciones de trekking y cursos de escalada. Seguridad, pasión y respeto por la naturaleza.
          </p>
          <div className="flex space-x-4">
            <Instagram className="h-5 w-5 hover:text-orange-500 cursor-pointer transition-colors" />
            <Facebook className="h-5 w-5 hover:text-orange-500 cursor-pointer transition-colors" />
            <Twitter className="h-5 w-5 hover:text-orange-500 cursor-pointer transition-colors" />
          </div>
        </div>

        <div>
          <h4 className="text-lg font-bold mb-6 text-orange-500">Explorar</h4>
          <ul className="space-y-3 text-sm text-gray-400">
            <li className="hover:text-white transition-colors cursor-pointer">Expediciones Pirineos</li>
            <li className="hover:text-white transition-colors cursor-pointer">Cursos de Escalada</li>
            <li className="hover:text-white transition-colors cursor-pointer">Guías Titulados</li>
            <li className="hover:text-white transition-colors cursor-pointer">Seguridad de Montaña</li>
          </ul>
        </div>

        <div>
          <h4 className="text-lg font-bold mb-6 text-orange-500">Legal</h4>
          <ul className="space-y-3 text-sm text-gray-400">
            <li className="hover:text-white transition-colors cursor-pointer">Términos y Condiciones</li>
            <li className="hover:text-white transition-colors cursor-pointer">Política de Privacidad</li>
            <li className="hover:text-white transition-colors cursor-pointer">Seguro de Actividad</li>
          </ul>
        </div>

        <div>
          <h4 className="text-lg font-bold mb-6 text-orange-500">Contacto</h4>
          <div className="space-y-4 text-sm text-gray-400">
            <div className="flex items-center space-x-3">
              <Phone className="h-4 w-4 text-orange-500" />
              <span>+34 600 000 000</span>
            </div>
            <div className="flex items-center space-x-3">
              <Mail className="h-4 w-4 text-orange-500" />
              <span>info@rocaysenda.com</span>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-4 mt-16 pt-8 border-t border-gray-700 text-center text-xs text-gray-500">
        &copy; {new Date().getFullYear()} Roca & Senda. Todos los derechos reservados. Creado con pasión por la montaña.
      </div>
    </footer>
  );
};

export default Footer;
