import React from 'react';
import './globals.css';
import { WalletProvider } from './components/providers/WalletProvider';

function Layout({ children }) {
  return (
    <div className="bg-gray-50 min-h-screen">
      <WalletProvider>
        {children}
      </WalletProvider>
    </div>
  );
}

export default Layout;