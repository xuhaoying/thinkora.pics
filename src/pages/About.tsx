import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Shield, Heart, Users, Zap, Award, Mail, ExternalLink, BookOpen, Lightbulb, Globe, Star } from 'lucide-react';
import { motion } from 'framer-motion';

const About = () => {
  const teamMembers = [
    {
      name: "AI Development Team",
      role: "Artificial Intelligence Engineers",
      description: "Experts in machine learning and computer vision, specializing in safe AI content generation for children.",
      avatar: "🤖",
      expertise: ["Machine Learning", "Computer Vision", "AI Safety", "Content Moderation"]
    },
    {
      name: "Child Development Specialists",
      role: "Educational Consultants",
      description: "Child psychologists and educators ensuring our content supports healthy development and learning.",
      avatar: "👩‍🏫",
      expertise: ["Child Psychology", "Early Education", "Creative Development", "Learning Design"]
    },
    {
      name: "Safety & Moderation Team",
      role: "Content Safety Officers",
      description: "Dedicated professionals monitoring and ensuring all generated content meets the highest safety standards.",
      avatar: "🛡️",
      expertise: ["Content Moderation", "Child Safety", "Policy Development", "Risk Assessment"]
    },
    {
      name: "Design & UX Team",
      role: "User Experience Designers",
      description: "Creating intuitive, accessible, and delightful experiences for parents, teachers, and children.",
      avatar: "🎨",
      expertise: ["UI/UX Design", "Accessibility", "User Research", "Visual Design"]
    }
  ];

  const values = [
    {
      icon: Shield,
      title: "Child Safety First",
      description: "Every piece of content is filtered through multiple safety layers to ensure it's appropriate for children."
    },
    {
      icon: Heart,
      title: "Educational Focus",
      description: "We believe coloring enhances creativity, motor skills, and cognitive development in children."
    },
    {
      icon: Sparkles,
      title: "Innovation with Purpose",
      description: "We use cutting-edge AI technology responsibly to create meaningful educational experiences."
    },
    {
      icon: Users,
      title: "Community Driven",
      description: "We listen to feedback from parents, teachers, and educators to continuously improve our service."
    }
  ];

  const achievements = [
    {
      icon: Award,
      number: "50,000+",
      label: "Coloring Pages Generated",
      description: "Trusted by families worldwide"
    },
    {
      icon: Shield,
      number: "99.9%",
      label: "Safety Rate",
      description: "Content passes safety checks"
    },
    {
      icon: Users,
      number: "10,000+",
      label: "Happy Families",
      description: "Parents and children love our service"
    },
    {
      icon: Zap,
      number: "< 30s",
      label: "Generation Time",
      description: "Fast, high-quality results"
    }
  ];

  const testimonials = [
    {
      quote: "Thinkora.pics has transformed how we engage with art in our classroom. The AI-generated coloring pages are perfect for different age groups and learning styles.",
      author: "Sarah Johnson",
      role: "Elementary School Teacher",
      avatar: "👩‍🏫"
    },
    {
      quote: "As a parent, I love how safe and educational the coloring pages are. My kids are always excited to see what they can create next!",
      author: "Michael Chen",
      role: "Parent of two",
      avatar: "👨‍👩‍👧‍👦"
    },
    {
      quote: "The quality and variety of coloring pages is incredible. It's become an essential tool in our art therapy sessions.",
      author: "Dr. Emily Rodriguez",
      role: "Child Psychologist",
      avatar: "👩‍⚕️"
    }
  ];

  const faqs = [
    {
      question: "How does the AI generate coloring pages?",
      answer: "Our AI uses advanced diffusion models specifically trained on child-appropriate line art. It understands prompts and creates clean, detailed coloring pages suitable for different age groups."
    },
    {
      question: "Is the content safe for children?",
      answer: "Yes! Every piece of content goes through multiple safety layers, including AI filtering, automated checks, and human moderation to ensure it's appropriate for children."
    },
    {
      question: "Can I use the coloring pages commercially?",
      answer: "Personal and educational use is included. For commercial use, please contact us for licensing options."
    },
    {
      question: "What age groups are the coloring pages suitable for?",
      answer: "We offer content for ages 3-13+, with different complexity levels and themes appropriate for each age group."
    }
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="py-24 px-4 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-white via-brand-50/30 to-purple-50/40 dark:from-surface-950 dark:via-surface-900 dark:to-surface-950"></div>
        <div className="absolute top-1/2 left-0 w-96 h-96 bg-gradient-to-r from-brand-400/10 to-purple-400/10 rounded-full blur-3xl"></div>
        
        <div className="relative max-w-6xl mx-auto text-center">
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            <div className="text-6xl mb-6">🎨</div>
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              About Thinkora.pics
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed">
              We're on a mission to revolutionize creative education through safe, intelligent, 
              and inspiring AI-generated coloring pages that spark imagination and learning in children aged 3-13+.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ x: -40, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
                Our Mission
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  At Thinkora.pics, we believe that creativity is the foundation of learning and development. 
                  Our AI-powered platform democratizes access to high-quality, educational coloring content 
                  that was previously only available through expensive design services.
                </p>
                <p>
                  We're committed to creating a safe, inclusive digital environment where children can explore 
                  their creativity while parents and educators have peace of mind knowing the content is 
                  appropriate and beneficial for young minds.
                </p>
                <p>
                  By combining advanced artificial intelligence with child development expertise, we're 
                  building the future of educational entertainment—one coloring page at a time.
                </p>
              </div>
            </motion.div>
            
            <motion.div
              initial={{ x: 40, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="bg-gradient-to-br from-brand-50 to-purple-50 dark:from-brand-950/20 dark:to-purple-950/20 rounded-3xl p-8 border border-brand-200 dark:border-brand-800"
            >
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                Why Coloring Matters
              </h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-brand-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-sm">✓</span>
                  </div>
                  <span className="text-gray-700 dark:text-gray-300">Develops fine motor skills and hand-eye coordination</span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-brand-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-sm">✓</span>
                  </div>
                  <span className="text-gray-700 dark:text-gray-300">Enhances focus, concentration, and patience</span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-brand-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-sm">✓</span>
                  </div>
                  <span className="text-gray-700 dark:text-gray-300">Stimulates creativity and self-expression</span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-brand-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-sm">✓</span>
                  </div>
                  <span className="text-gray-700 dark:text-gray-300">Provides therapeutic stress relief and mindfulness</span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-brand-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-sm">✓</span>
                  </div>
                  <span className="text-gray-700 dark:text-gray-300">Builds confidence through creative achievement</span>
                </li>
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-16 px-4 bg-gray-50 dark:bg-surface-900">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Our Core Values
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              These principles guide every decision we make and every feature we build
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {values.map((value, index) => (
              <motion.div
                key={index}
                initial={{ y: 40, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white dark:bg-surface-800 rounded-2xl p-8 shadow-sm border border-gray-200 dark:border-surface-700 hover:shadow-lg transition-shadow"
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-brand-100 dark:bg-brand-900/30 rounded-xl">
                    <value.icon className="h-6 w-6 text-brand-600 dark:text-brand-400" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                      {value.title}
                    </h3>
                    <p className="text-gray-700 dark:text-gray-300">
                      {value.description}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Meet Our Team
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Experts dedicated to creating safe, educational, and engaging experiences
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {teamMembers.map((member, index) => (
              <motion.div
                key={index}
                initial={{ y: 40, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white dark:bg-surface-800 rounded-2xl p-8 shadow-sm border border-gray-200 dark:border-surface-700"
              >
                <div className="flex items-start gap-4">
                  <div className="text-4xl">{member.avatar}</div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">
                      {member.name}
                    </h3>
                    <p className="text-brand-600 dark:text-brand-400 mb-3">
                      {member.role}
                    </p>
                    <p className="text-gray-700 dark:text-gray-300 mb-4">
                      {member.description}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {member.expertise.map((skill, skillIndex) => (
                        <span
                          key={skillIndex}
                          className="px-3 py-1 bg-brand-50 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400 rounded-full text-sm"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-16 px-4 bg-gray-50 dark:bg-surface-900">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Our Technology
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Powered by state-of-the-art AI models and child safety algorithms
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <motion.div
              initial={{ y: 40, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950/20 dark:to-cyan-950/20 rounded-2xl p-8 border border-blue-200 dark:border-blue-800"
            >
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                Advanced AI Models
              </h3>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                We utilize cutting-edge diffusion models specifically fine-tuned for generating 
                clean, child-appropriate line art that's perfect for coloring.
              </p>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>• Stable Diffusion XL for high-quality generation</li>
                <li>• Custom fine-tuning for line art style</li>
                <li>• Age-appropriate content filtering</li>
                <li>• Style consistency preservation</li>
              </ul>
            </motion.div>
            
            <motion.div
              initial={{ y: 40, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 rounded-2xl p-8 border border-green-200 dark:border-green-800"
            >
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                Safety Systems
              </h3>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                Multiple layers of content safety and moderation ensure every piece of content is appropriate for children.
              </p>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>• Real-time content filtering</li>
                <li>• Automated safety checks</li>
                <li>• Human moderation review</li>
                <li>• Age-appropriate categorization</li>
              </ul>
            </motion.div>
            
            <motion.div
              initial={{ y: 40, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/20 dark:to-pink-950/20 rounded-2xl p-8 border border-purple-200 dark:border-purple-800"
            >
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                Performance
              </h3>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                Optimized infrastructure ensures fast, reliable generation and delivery of coloring pages.
              </p>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>• Edge computing deployment</li>
                <li>• Automatic scaling</li>
                <li>• CDN distribution</li>
                <li>• Real-time monitoring</li>
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
              What Our Users Say
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Trusted by parents, teachers, and child development professionals
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ y: 40, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white dark:bg-surface-800 rounded-2xl p-8 shadow-sm border border-gray-200 dark:border-surface-700"
              >
                <div className="text-4xl mb-4">{testimonial.avatar}</div>
                <blockquote className="text-gray-700 dark:text-gray-300 mb-6">
                  "{testimonial.quote}"
                </blockquote>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {testimonial.author}
                  </p>
                  <p className="text-gray-600 dark:text-gray-400">
                    {testimonial.role}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 px-4 bg-gray-50 dark:bg-surface-900">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Everything you need to know about Thinkora.pics
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ y: 40, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white dark:bg-surface-800 rounded-2xl p-8 shadow-sm border border-gray-200 dark:border-surface-700"
              >
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                  {faq.question}
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  {faq.answer}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6 }}
            className="bg-gradient-to-br from-brand-500 to-purple-600 rounded-3xl p-12 text-center"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Start Creating?
            </h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Join thousands of parents and educators who are already using Thinkora.pics to inspire creativity and learning.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/generate"
                className="inline-flex items-center justify-center px-8 py-3 bg-white text-brand-600 font-semibold rounded-xl hover:bg-gray-50 transition-colors"
              >
                Start Creating
              </Link>
              <Link
                to="/gallery"
                className="inline-flex items-center justify-center px-8 py-3 bg-white/10 text-white font-semibold rounded-xl hover:bg-white/20 transition-colors"
              >
                View Gallery
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default About; 