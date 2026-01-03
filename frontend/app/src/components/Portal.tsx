import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';
import type { User } from '../services/authService';
import { api, type ClassData, type ResourceData, type MeetingData } from '../services/api';
import { ShootingStars } from './ui/shooting-stars';
import { StarsBackground } from './ui/stars-background';
import { FocusCards } from './ui/focus-cards';
import './Portal.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const resolveMediaUrl = (value?: string) => {
  if (!value) return undefined;
  if (/^https?:\/\//i.test(value)) return value;
  return `${API_BASE_URL}${value}`;
};

function Portal() {
  const [user, setUser] = useState<User | null>(null);
  const [classes, setClasses] = useState<ClassData[]>([]);
  const [resources, setResources] = useState<ResourceData[]>([]);
  const [meetings, setMeetings] = useState<MeetingData[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadUserData();
    loadPortalData();
    
    // Fallback timeout to prevent infinite loading
    const timeout = setTimeout(() => {
      console.log('Timeout: forcing loading to false');
      setLoading(false);
    }, 10000); // 10 seconds
    
    return () => clearTimeout(timeout);
  }, []);

  const loadUserData = async () => {
    try {
      const userData = authService.getUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to load user:', error);
      handleLogout();
    }
  };

  const loadPortalData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.log('No token found, redirecting to login');
        navigate('/login');
        return;
      }
      
      console.log('Fetching portal data with token...');
      
      // Fetch portal data (classes and resources)
      try {
        const data = await api.getMemberPortalData(token);
        console.log('Portal data received:', data);
        setClasses(Array.isArray(data?.classes) ? data.classes : []);
        setResources(Array.isArray(data?.resources) ? data.resources : []);
      } catch (portalError) {
        console.error('Failed to load portal data:', portalError);
        setClasses([]);
        setResources([]);
      }
      
      // Fetch meetings separately
      try {
        const meetingsData = await api.getMeetings(token);
        console.log('Meetings data received:', meetingsData);
        setMeetings(Array.isArray(meetingsData) ? meetingsData : []);
      } catch (meetingError) {
        console.error('Failed to load meetings:', meetingError);
        setMeetings([]);
      }
    } catch (error) {
      console.error('Failed to load portal data:', error);
      // Set empty data on error so page still loads
      setClasses([]);
      setResources([]);
      setMeetings([]);
    } finally {
      console.log('Setting loading to false');
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'upcoming': return 'badge-upcoming';
      case 'ongoing': return 'badge-ongoing';
      case 'completed': return 'badge-completed';
      default: return 'badge-default';
    }
  };

  const getDifficultyBadgeClass = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'badge-beginner';
      case 'intermediate': return 'badge-intermediate';
      case 'advanced': return 'badge-advanced';
      default: return 'badge-default';
    }
  };

  const getModeBadgeClass = (mode: string) => {
    switch (mode) {
      case 'online': return 'badge-online';
      case 'offline': return 'badge-offline';
      case 'hybrid': return 'badge-hybrid';
      default: return 'badge-default';
    }
  };

  const getMeetingStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'upcoming': return 'badge-upcoming';
      case 'ongoing': return 'badge-ongoing';
      case 'completed': return 'badge-completed';
      case 'cancelled': return 'badge-cancelled';
      default: return 'badge-default';
    }
  };

  // Filter classes to show (memoized for display)
  const filteredClasses = classes.filter((classItem) => {
    if (!classItem) return false;
    // Show all classes except those completed more than 12 hours ago
    if (classItem.status_display === 'Completed' && classItem.end_date) {
      const endDate = new Date(classItem.end_date);
      const now = new Date();
      const hoursDiff = (now.getTime() - endDate.getTime()) / (1000 * 60 * 60);
      return hoursDiff < 12;
    }
    return true;
  });

  // Filter meetings to show (memoized for display)
  const filteredMeetings = meetings.filter((meeting) => {
    if (!meeting) return false;
    // Hide completed meetings older than 2 hours
    if (meeting.computed_status === 'completed' && meeting.end_time) {
      const endDate = new Date(meeting.end_time);
      const now = new Date();
      const hoursDiff = (now.getTime() - endDate.getTime()) / (1000 * 60 * 60);
      return hoursDiff < 2;
    }
    // Hide cancelled meetings
    if (meeting.computed_status === 'cancelled') return false;
    return true;
  });

  // Filter resources to show
  const filteredResources = resources.filter((resource) => resource != null);

  const handleDownload = async (resourceId: number, downloadUrl: string) => {
    try {
      console.log('Download clicked for resource:', resourceId);
      const token = localStorage.getItem('access_token');
      if (token) {
        console.log('Incrementing download count...');
        // Increment download count
        const result = await api.incrementDownload(resourceId, token);
        console.log('Download count incremented:', result);
        
        // Update local state
        setResources(prevResources => 
          prevResources.map(r => 
            r.id === resourceId 
              ? { ...r, download_count: r.download_count + 1 }
              : r
          )
        );
      } else {
        console.error('No token found');
      }
      
      // Open download link
      window.open(downloadUrl, '_blank');
    } catch (error) {
      console.error('Failed to track download:', error);
      // Still open the download even if tracking fails
      window.open(downloadUrl, '_blank');
    }
  };

  if (loading) {
    return (
      <div className="portal-container" style={{ 
        minHeight: '100vh', 
        width: '100%',
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center' 
      }}>
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading portal...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="portal-container">
      <ShootingStars />
      <StarsBackground />
      <nav className="portal-navbar">
        <div className="navbar-brand">
          <h1>TARS Member Portal</h1>
        </div>
        <div className="navbar-user">
          <span className="user-name">
            Welcome, {user?.first_name || user?.username}!
          </span>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </nav>

      <main className="portal-content">
        {/* Classes Section */}
        <section className="portal-section">
          <div className="section-header">
            <h2>📚 Available Classes</h2>
          </div>

          {filteredClasses.length === 0 ? (
            <div className="empty-state">
              <p>No classes available at the moment.</p>
              <p className="text-muted">Check back later for new workshops and training sessions!</p>
            </div>
          ) : (
            <FocusCards cards={filteredClasses.map((classItem) => ({
              title: classItem.title || 'Untitled Class',
              src: resolveMediaUrl(classItem.thumbnail) || 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800',
              description: classItem.description || 'No description available',
              badges: (
                <>
                  <span className={`badge ${getStatusBadgeClass(classItem.status || 'upcoming')}`}>
                    {classItem.status_display || 'Scheduled'}
                  </span>
                  <span className={`badge ${getDifficultyBadgeClass(classItem.difficulty || 'beginner')}`}>
                    {classItem.difficulty_display || 'Beginner'}
                  </span>
                  <span className={`badge ${getModeBadgeClass(classItem.mode || 'online')}`}>
                    {classItem.mode_display || 'Online'}
                  </span>
                </>
              ),
              meta: (
                <>
                  <div className="meta-item">
                    <span className="meta-icon">👨‍🏫</span>
                    <span>{classItem.instructor_display || 'TBA'}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-icon">📅</span>
                    <span>{classItem.start_date_formatted || 'Date TBA'}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-icon">⏱️</span>
                    <span>{classItem.duration || 'TBA'}</span>
                  </div>
                  {(classItem.mode === 'offline' || classItem.mode === 'hybrid') && classItem.location && (
                    <div className="meta-item">
                      <span className="meta-icon">📍</span>
                      <span>{classItem.location}</span>
                    </div>
                  )}
                </>
              ),
              actions: (
                <>
                  {classItem.meeting_link && classItem.is_joinable ? (
                    <a 
                      href={classItem.meeting_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-primary"
                    >
                      Join Class
                    </a>
                  ) : classItem.meeting_link ? (
                    <button 
                      disabled
                      className="btn btn-primary"
                      title={classItem.status_display === 'Upcoming' ? 'Class has not started yet' : 'Class has ended'}
                    >
                      Join Class
                    </button>
                  ) : null}
                  {classItem.syllabus && (
                    <a 
                      href={resolveMediaUrl(classItem.syllabus)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-secondary"
                    >
                      View Syllabus
                    </a>
                  )}
                </>
              )
            }))} />
          )}
        </section>

        {/* Meetings Section */}
        <section className="portal-section">
          <div className="section-header">
            <h2>📅 Scheduled Meetings</h2>
          </div>

          {filteredMeetings.length === 0 ? (
            <div className="empty-state">
              <p>No meetings scheduled at the moment.</p>
              <p className="text-muted">Check back later for upcoming meetings and sessions!</p>
            </div>
          ) : (
            <FocusCards cards={filteredMeetings.map((meeting) => ({
              title: meeting.title || 'Untitled Meeting',
              src: 'https://images.unsplash.com/photo-1552581234-26160f608093?w=800',
              description: meeting.description || 'No description provided',
              badges: (
                <>
                  <span className={`badge ${getMeetingStatusBadgeClass(meeting.computed_status || 'upcoming')}`}>
                    {meeting.status_display || 'Scheduled'}
                  </span>
                  {meeting.is_for_all_domains ? (
                    <span className="badge badge-all-domains">All Members</span>
                  ) : (
                    (meeting.domains_detail || []).map(domain => (
                      <span key={domain.id} className="badge badge-domain">{domain.display_name}</span>
                    ))
                  )}
                </>
              ),
              meta: (
                <>
                  <div className="meta-item">
                    <span className="meta-icon">🎤</span>
                    <span>{meeting.speaker_name || 'TBA'}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-icon">📅</span>
                    <span>{meeting.scheduled_date_formatted || 'Date TBA'}</span>
                  </div>
                  {meeting.duration_minutes && (
                    <div className="meta-item">
                      <span className="meta-icon">⏱️</span>
                      <span>{meeting.duration_minutes} mins</span>
                    </div>
                  )}
                  {meeting.location && (
                    <div className="meta-item">
                      <span className="meta-icon">📍</span>
                      <span>{meeting.location}</span>
                    </div>
                  )}
                </>
              ),
              actions: (
                <>
                  {meeting.meeting_link && (meeting.computed_status === 'upcoming' || meeting.computed_status === 'ongoing') && (
                    <a 
                      href={meeting.meeting_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-primary"
                    >
                      {meeting.computed_status === 'ongoing' ? 'Join Now' : 'Join Meeting'}
                    </a>
                  )}
                </>
              )
            }))} />
          )}
        </section>

        {/* Resources Section */}
        <section className="portal-section">
          <div className="section-header">
            <h2>📖 Learning Resources</h2>
          </div>

          {filteredResources.length === 0 ? (
            <div className="empty-state">
              <p>No resources available at the moment.</p>
              <p className="text-muted">Check back later for tutorials, documentation, and learning materials!</p>
            </div>
          ) : (
            <FocusCards cards={filteredResources.map((resource) => ({
              title: resource.title || 'Untitled Resource',
              src: resolveMediaUrl(resource.thumbnail) || 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800',
              description: resource.description || 'No description available',
              badges: (
                <>
                  <span className="badge badge-category">{resource.category_display || 'Resource'}</span>
                  {resource.is_featured && (
                    <span className="badge badge-featured">⭐ Featured</span>
                  )}
                </>
              ),
              meta: resource.author ? (
                <div className="meta-item">
                  <span className="meta-icon">✍️</span>
                  <span>{resource.author}</span>
                </div>
              ) : undefined,
              tags: resource.tag_list || [],
              actions: (
                <>
                  {resource.external_link && (
                    <button
                      onClick={() => handleDownload(resource.id, resource.external_link || '')}
                      className="btn btn-primary"
                    >
                      Visit Resource
                    </button>
                  )}
                  {resource.file && (
                    <button
                      onClick={() => handleDownload(resource.id, resolveMediaUrl(resource.file) || '')}
                      className="btn btn-secondary"
                    >
                      Download
                    </button>
                  )}
                </>
              )
            }))} />
          )}
        </section>
      </main>
    </div>
  );
}

export default Portal;
