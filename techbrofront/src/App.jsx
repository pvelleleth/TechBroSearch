import React from 'react';
import Sidebar from './components/Sidebar';
import SearchSection from './components/SearchSection';

function App() {
    return (
        <div className="flex w-full min-h-screen bg-light">
            <main className="flex-1 flex flex-col justify-center items-center ml-[10px] w-[calc(100%-250px)] min-h-screen relative px-8">
                <SearchSection />
            </main>
        </div>
    );
}

export default App;