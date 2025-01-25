import React, { useState } from 'react';
import { FaLinkedin } from 'react-icons/fa';

const mockLeads = [
    {
        name: "Daniel Walker",
        company: "Viking Industrial Painting",
        position: "Head of Procurement at Viking Industrial Painting",
        phone: "402-637-4575",
        email: "daniel@viptanks.com",
        linkedin: "https://www.linkedin.com/in/daniel-walker-2ba193171/"
    },
    {
        name: "Ryan Rood",
        company: "JC Toland Painting",
        position: "Project Manager",
        phone: "515-782-0051",
        email: "ryan.rood@jctolandpainting.com",
        linkedin: "https://www.linkedin.com/in/ryan-rood-80455aab/"
    },
    {
        name: "Rhonda Waddle",
        company: "Dayco",
        position: "Indirect Purchasing Manager",
        phone: "248-404-6500",
        email: "",
        linkedin: "https://www.linkedin.com/in/rhonda-waddle-87a340135/"
    },
    {
        name: "Susan Boyd",
        company: "Vulcan Painters",
        position: "Director of Communications",
        phone: "205-428-0556",
        email: "",
        linkedin: "https://www.linkedin.com/in/susan-boyd-3b94a64b/"
    },
    {
        name: "Amanda Martin",
        company: "Porta-Painting",
        position: "President",
        phone: "262-970-9713",
        email: "amanda.m@portapainting.com",
        linkedin: "https://www.linkedin.com/in/amanda-martin-66b41996"
    },
    {
        name: "Jason Gums",
        company: "Carbit Paint Company",
        position: "Purchasing Agent",
        phone: "773-287-9200",
        email: "jason.gums@carbit.com",
        linkedin: "https://www.linkedin.com/in/jason-gums-254b35179"
    },
    {
        name: "Michael Chen",
        company: "Midwest Coating Consultants",
        position: "Supply Chain Manager",
        phone: "816-474-1616",
        email: "mchen@midwestcoatings.com",
        linkedin: "https://www.linkedin.com/in/michael-chen-coating"
    },
    {
        name: "Lisa Rodriguez",
        company: "Induspray",
        position: "Purchasing Coordinator",
        phone: "877-568-8877",
        email: "lisa.r@induspray.com",
        linkedin: "https://www.linkedin.com/in/lisa-rodriguez-induspray"
    },
    {
        name: "David Thompson",
        company: "Painters USA",
        position: "Procurement Specialist",
        phone: "800-999-8715",
        email: "d.thompson@paintersusa.com",
        linkedin: "https://www.linkedin.com/in/david-thompson-painterusa"
    },
    {
        name: "Tim Schrieber",
        company: "1st Phorm International",
        position: "Design & Procurement Mgr.",
        phone: "636-326-6200",
        email: "tim.s@1stphorm.com",
        linkedin: "https://www.linkedin.com/in/tim-schrieber-58304a69"
    },
    {
        name: "Sarah Johnson",
        company: "CertaPro Painters",
        position: "Materials Manager",
        phone: "866-441-6758",
        email: "sjohnson@certapro.com",
        linkedin: "https://www.linkedin.com/in/sarah-johnson-certapro"
    },
    {
        name: "Robert Anderson",
        company: "Sherwin-Williams",
        position: "Sourcing Manager",
        phone: "216-566-2000",
        email: "r.anderson@sherwin.com",
        linkedin: "https://www.linkedin.com/in/robert-anderson-sherwin"
    },
    {
        name: "Emily Parker",
        company: "Benjamin Moore",
        position: "Procurement Director",
        phone: "201-573-9600",
        email: "emily.parker@benjaminmoore.com",
        linkedin: "https://www.linkedin.com/in/emily-parker-bmoore"
    },
    {
        name: "Mark Stevens",
        company: "PPG Industries",
        position: "Supply Chain Specialist",
        phone: "412-434-3131",
        email: "mstevens@ppg.com",
        linkedin: "https://www.linkedin.com/in/mark-stevens-ppg"
    },
    {
        name: "Laura Thompson",
        company: "Behr Paint Company",
        position: "Purchasing Manager",
        phone: "714-545-7101",
        email: "l.thompson@behr.com",
        linkedin: "https://www.linkedin.com/in/laura-thompson-behr"
    },
    {
        name: "Chris Wilson",
        company: "Valspar Corporation",
        position: "Procurement Analyst",
        phone: "612-851-7000",
        email: "chris.wilson@valspar.com",
        linkedin: "https://www.linkedin.com/in/chris-wilson-valspar"
    },
    {
        name: "Jessica Lee",
        company: "Kelly-Moore Paints",
        position: "Supply Chain Coordinator",
        phone: "650-330-1200",
        email: "j.lee@kellymoore.com",
        linkedin: "https://www.linkedin.com/in/jessica-lee-kellymoore"
    },
    {
        name: "Brian Miller",
        company: "Dunn-Edwards Corporation",
        position: "Sourcing Specialist",
        phone: "323-826-3600",
        email: "brian.m@dunnedwards.com",
        linkedin: "https://www.linkedin.com/in/brian-miller-dunnedwards"
    },
    {
        name: "Karen White",
        company: "Pratt & Lambert",
        position: "Procurement Officer",
        phone: "216-566-2902",
        email: "k.white@prattandlambert.com",
        linkedin: "https://www.linkedin.com/in/karen-white-prattlambert"
    },
    {
        name: "Thomas Brown",
        company: "Rust-Oleum",
        position: "Purchasing Supervisor",
        phone: "847-367-7700",
        email: "t.brown@rustoleum.com",
        linkedin: "https://www.linkedin.com/in/thomas-brown-rustoleum"
    }
];


const SearchSection = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [leads, setLeads] = useState([]);
    const [showResults, setShowResults] = useState(false);
    const [followUpQuestion, setFollowUpQuestion] = useState('');
    const [qualifyingLeads, setQualifyingLeads] = useState(new Set());

    const handleSearch = async () => {
        setIsLoading(true);
        setShowResults(false);
        await new Promise(resolve => setTimeout(resolve, 2000));
        setLeads(mockLeads);
        setIsLoading(false);
        setShowResults(true);
    };

    const handleQualify = (leadIndex) => {
        setQualifyingLeads(prev => {
            const newSet = new Set(prev);
            newSet.add(leadIndex);
            return newSet;
        });
        // Here you would typically make an API call to update the lead status
    };

    const handleQualifyAll = () => {
        // Add all lead indices to the qualifyingLeads set
        const allIndices = new Set(leads.map((_, index) => index));
        setQualifyingLeads(allIndices);
        // Here you would typically make an API call to update all leads' status
        
        // Optional: Reset after some time (remove if you want to keep the qualifying state)
        // setTimeout(() => setQualifyingLeads(new Set()), 2000);
    };

    return (
        <div className="w-full max-w-[1000px] flex flex-col items-center font-inter relative pt-8">
            <h1 className="text-5xl mb-6 text-center font-poppins font-light text-gray-900 tracking-tight">
                Find Tech Bros
            </h1>

            <div className="w-full bg-white rounded-lg p-4 shadow-md border border-gray-200">
                <input
                    type="text"
                    className="w-full p-4 bg-transparent border-none text-gray-900 text-lg font-inter 
                        placeholder-gray-500 focus:outline-none"
                    placeholder="Ask anything..."
                />
                <div className="flex justify-end pt-2">
                    <button 
                        onClick={handleSearch}
                        className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors"
                    >
                        Ask
                    </button>
                </div>
            </div>

            {isLoading && (
                <div className="mt-8 flex items-center gap-2 text-blue-600">
                    <div className="text-xl">Thinking</div>
                    <div className="flex">
                        <span className="animate-bounce delay-0">.</span>
                        <span className="animate-bounce delay-150">.</span>
                        <span className="animate-bounce delay-300">.</span>
                    </div>
                </div>
            )}

            {showResults && (
                <div className="mt-8 w-full">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {leads.map((lead, index) => (
                            <div key={index} 
                                className="bg-white rounded-xl p-6 hover:bg-gray-50 transition-all 
                                    duration-300 group shadow-sm border border-gray-200">
                                <div className="mb-4">
                                    <div className="flex justify-between items-start">
                                        <h3 className="text-lg font-medium text-gray-900 
                                            group-hover:text-blue-600 transition-colors">
                                            {lead.name}
                                        </h3>
                                        <button
                                            onClick={() => handleQualify(index)}
                                            disabled={qualifyingLeads.has(index)}
                                            className={`px-3 py-1 rounded-lg text-sm font-medium transition-all duration-300 ${
                                                qualifyingLeads.has(index)
                                                ? 'bg-blue-100 text-blue-600 cursor-not-allowed'
                                                : 'bg-blue-600 text-white hover:bg-blue-700'
                                            }`}
                                        >
                                            {qualifyingLeads.has(index) ? 'Qualifying...' : 'Qualify'}
                                        </button>
                                    </div>
                                    <div className="mt-2 space-y-2">
                                        <div className="bg-gray-100 text-gray-800 px-3 py-1 
                                            rounded-full text-sm inline-block">
                                            {lead.company}
                                        </div>
                                        <div className="text-gray-600 text-sm">{lead.position}</div>
                                    </div>
                                </div>
                                
                                <div className="flex flex-wrap items-center gap-2">
                                    {lead.email && (
                                        <a href={`mailto:${lead.email}`} 
                                           className="flex items-center gap-2 bg-gray-100 px-3 py-1.5 
                                            rounded-lg text-gray-800 hover:bg-gray-200 
                                            transition-colors group/btn">
                                            <svg xmlns="http://www.w3.org/2000/svg" 
                                                className="h-4 w-4 group-hover/btn:scale-110 transition-transform" 
                                                viewBox="0 0 24 24" fill="currentColor">
                                                <path d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 5.493a3 3 0 01-3.144 0L1.5 8.67z" />
                                                <path d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 5.978a1.5 1.5 0 001.572 0L22.5 6.908z" />
                                            </svg>
                                            <span className="text-sm">Email</span>
                                        </a>
                                    )}
                                    {lead.phone && (
                                        <a href={`tel:${lead.phone}`} 
                                           className="flex items-center gap-2 bg-gray-100 px-3 py-1.5 
                                            rounded-lg text-gray-800 hover:bg-gray-200 
                                            transition-colors group/btn">
                                            <svg xmlns="http://www.w3.org/2000/svg" 
                                                className="h-4 w-4 group-hover/btn:scale-110 transition-transform" 
                                                viewBox="0 0 24 24" fill="currentColor">
                                                <path fillRule="evenodd" d="M1.5 4.5a3 3 0 013-3h1.372c.86 0 1.61.586 1.819 1.42l1.105 4.423a1.875 1.875 0 01-.694 1.955l-1.293.97c-.135.101-.164.249-.126.352a11.285 11.285 0 006.697 6.697c.103.038.25.009.352-.126l.97-1.293a1.875 1.875 0 011.955-.694l4.423 1.105c.834.209 1.42.959 1.42 1.82V19.5a3 3 0 01-3 3h-2.25C8.552 22.5 1.5 15.448 1.5 6.75V4.5z" clipRule="evenodd" />
                                            </svg>
                                            <span className="text-sm">Call</span>
                                        </a>
                                    )}
                                    <a href={lead.linkedin} 
                                       target="_blank" 
                                       rel="noopener noreferrer" 
                                       className="flex items-center gap-2 bg-gray-100 px-3 py-1.5 
                                        rounded-lg text-gray-800 hover:bg-gray-200 
                                        transition-colors group/btn">
                                        <FaLinkedin className="h-4 w-4 group-hover/btn:scale-110 transition-transform" />
                                        <span className="text-sm">Profile</span>
                                    </a>
                                </div>
                            </div>
                        ))}
                    </div>
                    
                    <div className="mt-4 mb-8 flex justify-end items-center gap-4">
                        <input
                            type="text"
                            value={followUpQuestion}
                            onChange={(e) => setFollowUpQuestion(e.target.value)}
                            placeholder="Follow-up request..."
                            className="flex-grow p-2 rounded-md bg-white text-gray-900 
                                border border-gray-300 focus:outline-none focus:border-blue-600"
                        />
                        <button
                            onClick={handleQualifyAll}
                            className="bg-blue-600 text-white px-6 py-2 rounded-md 
                                hover:bg-blue-700 transition-colors"
                        >
                            Qualify All Leads
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SearchSection;