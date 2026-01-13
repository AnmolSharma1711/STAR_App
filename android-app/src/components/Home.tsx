import { useState, useEffect, type MouseEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { ShootingStars } from './ui/shooting-stars'
import { StarsBackground } from './ui/stars-background'
import './Home.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const resolveMediaUrl = (value?: string) => {
  if (!value) return undefined
  if (/^https?:\/\//i.test(value)) return value
  return `${API_BASE_URL}${value}`
}

interface SiteSettings {
  id: number
  club_name: string
  club_full_name: string
  club_motto: string
  club_logo?: string
  university_logo?: string
  hero_background?: string
}

interface Sponsor {
  id: number
  name: string
  logo: string
  website?: string
  collaboration_agenda: string
  collaboration_date: string
  collaboration_date_formatted: string
  order: number
}

interface SocialLink {
  id: number
  platform: string
  platform_display: string
  url: string
  icon_class?: string
  order: number
}

interface TeamMember {
  id: number
  name: string
  role: 'mentor' | 'lead'
  role_display: string
  position: string
  email?: string | null
  quote?: string | null
  tech_stack?: string | null
  image?: string | null
  linkedin_url?: string | null
  github_url?: string | null
  twitter_url?: string | null
  instagram_url?: string | null
  website_url?: string | null
  order: number
}

interface HomePageData {
  site_settings: SiteSettings | null
  sponsors: Sponsor[]
  mentors: TeamMember[]
  leads: TeamMember[]
  social_links: SocialLink[]
}

const Home = () => {
  const navigate = useNavigate()
  const [homeData, setHomeData] = useState<HomePageData | null>(null)
  const [loading, setLoading] = useState(true)
  const [flippedCards, setFlippedCards] = useState<Record<string, boolean>>({})

  useEffect(() => {
    fetchHomeData()
  }, [])

  const fetchHomeData = async () => {
    try {
      const data = await api.getHomePageData()
      setHomeData(data)
    } catch (error) {
      console.error('Failed to load home page data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="home-loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  const settings = homeData?.site_settings

  const toggleCard = (key: string) => {
    setFlippedCards((prev) => ({ ...prev, [key]: !prev[key] }))
  }

  const stopPropagation = (e: MouseEvent<HTMLElement>) => {
    e.stopPropagation()
  }

  const renderTeamRow = (title: string, members: TeamMember[]) => {
    if (!members || members.length === 0) return null
    const rowItems = (members.length < 5
      ? [...members, ...members, ...members]
      : members
    )

    return (
      <div className="team-row">
        <h3 className="team-row-title">{title}</h3>
        <div className="team-scroll-wrapper">
          <div className="team-scroll">
            {rowItems.map((member, index) => {
              const key = `${member.id}-${index}`
              const isFlipped = !!flippedCards[key]

              return (
                <button
                  key={key}
                  type="button"
                  className={`team-card ${isFlipped ? 'is-flipped' : ''}`}
                  onClick={() => toggleCard(key)}
                  aria-pressed={isFlipped}
                >
                  <div className="team-card-inner">
                    <div className="team-card-face team-card-front">
                      <div className="team-avatar-wrapper">
                        {member.image ? (
                          <img
                            src={resolveMediaUrl(member.image)}
                            alt={member.name}
                            className="team-avatar"
                          />
                        ) : (
                          <div className="team-avatar-placeholder">{member.name?.[0] || '?'}</div>
                        )}
                      </div>
                      <div className="team-front-info">
                        <div className="team-name">{member.name}</div>
                        <div className="team-position">{member.position}</div>
                      </div>
                    </div>

                    <div className="team-card-face team-card-back">
                      <div className="team-back-top">
                        <div className="team-name">{member.name}</div>
                        <div className="team-position">{member.position}</div>
                      </div>

                      {member.quote && (
                        <div className="team-quote">“{member.quote}”</div>
                      )}

                      {member.tech_stack && (
                        <div className="team-tech">
                          <span className="team-tech-label">Tech:</span> {member.tech_stack}
                        </div>
                      )}

                      {member.email && (
                        <a
                          className="team-email"
                          href={`mailto:${member.email}`}
                          onClick={stopPropagation}
                        >
                          {member.email}
                        </a>
                      )}

                      <div className="team-socials">
                        {member.linkedin_url && (
                          <a href={member.linkedin_url} target="_blank" rel="noopener noreferrer" onClick={stopPropagation}>
                            💼
                          </a>
                        )}
                        {member.github_url && (
                          <a href={member.github_url} target="_blank" rel="noopener noreferrer" onClick={stopPropagation}>
                            💻
                          </a>
                        )}
                        {member.twitter_url && (
                          <a href={member.twitter_url} target="_blank" rel="noopener noreferrer" onClick={stopPropagation}>
                            🐦
                          </a>
                        )}
                        {member.instagram_url && (
                          <a href={member.instagram_url} target="_blank" rel="noopener noreferrer" onClick={stopPropagation}>
                            📷
                          </a>
                        )}
                        {member.website_url && (
                          <a href={member.website_url} target="_blank" rel="noopener noreferrer" onClick={stopPropagation}>
                            🌐
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                </button>
              )
            })}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="home-container">
      <ShootingStars />
      <StarsBackground />
      
      {settings?.university_logo && (
        <div className="university-logo-wrapper">
          <img 
            src={resolveMediaUrl(settings.university_logo)}
            alt="University Logo"
            className="university-logo"
          />
        </div>
      )}

      {/* Hero Section */}
      <section 
        className="hero-section"
        style={{
          backgroundImage: settings?.hero_background 
            ? `linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%), url(${resolveMediaUrl(settings.hero_background)})`
            : undefined,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        <div className="hero-content">
          {settings?.club_logo && (
            <div className="hero-logo">
              <img 
                src={resolveMediaUrl(settings.club_logo)}
                alt={settings.club_name}
                className="club-logo-img"
              />
            </div>
          )}
          <h1 className="hero-title">{settings?.club_name || 'TARS'}</h1>
          <h2 className="hero-subtitle">
            {settings?.club_full_name || 'Technology and Automation Research Society'}
          </h2>
          <p className="hero-motto">
            {settings?.club_motto || 
              'Pioneering the future of intelligent systems and automated solutions. Innovating at the intersection of technology, research, and human advancement.'}
          </p>
          <div className="hero-actions">
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/login')}
            >
              Member Login
            </button>
            <button 
              className="btn btn-secondary"
              onClick={() => document.querySelector('.team-section')?.scrollIntoView({ behavior: 'smooth' })}
            >
              Mentors & Leads
            </button>
          </div>
        </div>
      </section>

      {/* Mentors & Leads Section */}
      {(homeData?.mentors?.length || homeData?.leads?.length) ? (
        <section className="team-section">
          <div className="team-container">
            <h2 className="section-title">Mentors & Leads</h2>
            <p className="section-subtitle">Meet the people guiding the club</p>
            {renderTeamRow('Mentors', homeData?.mentors || [])}
            {renderTeamRow('Leads', homeData?.leads || [])}
          </div>
        </section>
      ) : null}

      {/* Footer */}
      <footer className="home-footer">
        <div className="footer-content">
          <div className="footer-section">
              {settings?.club_logo && (
                <img 
                  src={resolveMediaUrl(settings.club_logo)}
                  alt={settings.club_name}
                  className="footer-logo"
                />
              )}
            <h3>{settings?.club_name || 'TARS'}</h3>
            <p>{settings?.club_full_name || 'Technology and Automation Research Society'}</p>
          </div>
          
          {homeData?.social_links && homeData.social_links.length > 0 && (
            <div className="footer-section">
              <h4>Connect With Us</h4>
              <div className="social-links">
                {homeData.social_links.map((link) => (
                  <a
                    key={link.id}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="social-link"
                    title={link.platform_display}
                  >
                    {link.platform === 'facebook' && '📘'}
                    {link.platform === 'twitter' && '🐦'}
                    {link.platform === 'instagram' && '📷'}
                    {link.platform === 'linkedin' && '💼'}
                    {link.platform === 'github' && '💻'}
                    {link.platform === 'youtube' && '📺'}
                    {link.platform === 'discord' && '💬'}
                    {link.platform === 'email' && '📧'}
                    {link.platform === 'website' && '🌐'}
                    {link.platform === 'other' && '🔗'}
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>

        {homeData?.sponsors && homeData.sponsors.length > 0 && (
          <div className="footer-sponsors">
            <h4 className="footer-sponsors-title">Sponsors</h4>
            <div className="footer-sponsor-logos">
              {homeData.sponsors.map((sponsor) => (
                <a
                  key={sponsor.id}
                  href={sponsor.website || '#'}
                  target={sponsor.website ? '_blank' : undefined}
                  rel={sponsor.website ? 'noopener noreferrer' : undefined}
                  className={`footer-sponsor-logo-link ${sponsor.website ? '' : 'is-disabled'}`}
                  aria-label={sponsor.website ? `${sponsor.name} website` : sponsor.name}
                  onClick={(e) => {
                    if (!sponsor.website) e.preventDefault()
                  }}
                >
                  <img
                    src={resolveMediaUrl(sponsor.logo)}
                    alt={sponsor.name}
                    className="footer-sponsor-logo"
                  />
                </a>
              ))}
            </div>
          </div>
        )}

        <p className="footer-copyright">
          © {new Date().getFullYear()} {settings?.club_name || 'TARS'}. All rights reserved.
        </p>
      </footer>
    </div>
  )
}

export default Home
