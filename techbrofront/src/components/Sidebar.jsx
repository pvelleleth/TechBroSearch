import React, { useState } from 'react';
import { FaHome, FaUsers, FaBook } from 'react-icons/fa';
import { HiOutlinePaperAirplane } from "react-icons/hi2";
import { MdPerson2 } from "react-icons/md";
import { NavLink } from 'react-router';

const Sidebar = () => {
    const [collapsed, setCollapsed] = useState(false);

    const toggleSidebar = () => {
        setCollapsed(!collapsed);
    };

    return (
        <div className={`bg-white h-screen p-5 flex flex-col justify-between fixed overflow-y-auto 
            transition-width duration-300 shadow-[6px_0_20px_-3px_rgba(0,0,0,0.1)] border-r border-gray-200
            ${collapsed ? 'w-[80px]' : 'w-[250px]'}`}>
            <div>
                <div className="flex items-center gap-3 mb-5 cursor-pointer" onClick={toggleSidebar}>
                    <div className="tw-h-[50px] tw-max-w-[250px]">
                    <div className="text-gray-600 text-4xl">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="4" r="2" />
                            <line x1="12" y1="6" x2="12" y2="14" />
                            <line x1="12" y1="14" x2="8" y2="20" />
                            <line x1="12" y1="14" x2="16" y2="20" />
                        </svg>
                    </div>
                    </div>
                </div>
                <nav>
                    <ul className="list-none p-0">
                        <NavLink to="/" className={({ isActive }) => 
                            `my-5 cursor-pointer font-inter text-black hover:text-blue-600 
                            transition-colors hover:scale-105 flex items-center gap-2
                            ${isActive ? 'text-blue-600' : ''}`}>
                            <FaHome />
                            {!collapsed && 'Home'}
                        </NavLink>
                        <NavLink to="/leads" className={({ isActive }) => 
                            `my-5 cursor-pointer font-inter text-black hover:text-blue-600 
                            transition-colors hover:scale-105 flex items-center gap-2
                            ${isActive ? 'text-blue-600' : ''}`}>
                            <HiOutlinePaperAirplane />
                            {!collapsed && 'Leads'}
                        </NavLink>
                        <li className="my-5 cursor-pointer font-inter text-black hover:text-blue-600 
                            transition-colors hover:scale-105 flex items-center gap-2">
                            <FaBook />
                            {!collapsed && 'Library'}
                        </li>
                    </ul>
                </nav>
            </div>
            <div className="flex items-center gap-3 mt-5">
                <MdPerson2 className="text-white text-4xl" />
                {!collapsed && (
                    <div>
                        <p className="text-white font-poppins">John Doe</p>
                        <p className="text-gray-400 text-sm">View Profile</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Sidebar;