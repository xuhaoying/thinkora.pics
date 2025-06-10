import React from 'react';
import { Shield, Lock, Cookie, Database, Clock, Globe, Mail, FileText } from 'lucide-react';

const PrivacyPolicy = () => {
  const dataRetentionPeriods = [
    {
      category: "Account Information",
      period: "Until account deletion",
      description: "Kept as long as your account is active"
    },
    {
      category: "Generated Content",
      period: "30 days",
      description: "Temporarily stored for service improvement"
    },
    {
      category: "Usage Analytics",
      period: "12 months",
      description: "Anonymized after 3 months"
    },
    {
      category: "Payment Information",
      period: "7 years",
      description: "Required for tax and legal compliance"
    }
  ];

  const cookieTypes = [
    {
      type: "Essential",
      purpose: "Required for basic website functionality",
      duration: "Session",
      examples: ["Authentication", "Security", "Basic preferences"]
    },
    {
      type: "Analytics",
      purpose: "Help us understand how visitors use our site",
      duration: "2 years",
      examples: ["Page views", "Feature usage", "Performance metrics"]
    },
    {
      type: "Preferences",
      purpose: "Remember your settings and preferences",
      duration: "1 year",
      examples: ["Language", "Theme", "Content filters"]
    }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white dark:bg-surface-800 rounded-xl shadow-sm border border-gray-200 dark:border-surface-700 p-8">
        <div className="text-center mb-8">
          <div className="text-4xl mb-4">🔒</div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Privacy Policy</h1>
          <p className="text-gray-600 dark:text-gray-300">
            Your privacy and your child's safety are our top priorities
          </p>
        </div>
        
        <div className="prose prose-gray max-w-none dark:prose-invert">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 p-4 bg-gray-50 dark:bg-surface-900 rounded-lg">
            <strong>Effective Date:</strong> {new Date().toLocaleDateString()} | 
            <strong> Last Updated:</strong> {new Date().toLocaleDateString()}
          </p>

          <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6 mb-8">
            <h2 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3 flex items-center gap-2">
              <Shield className="h-5 w-5" /> Child Safety Promise
            </h2>
            <p className="text-blue-800 dark:text-blue-200">
              Thinkora.pics is designed for adults (parents, teachers, caregivers) to create content for children. 
              We do not collect any personal information from children under 13, and all our content is thoroughly 
              moderated to ensure child safety and appropriateness.
            </p>
          </div>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Database className="h-5 w-5" /> 1. Information We Collect
            </h2>
            <div className="space-y-6 text-gray-700 dark:text-gray-300">
              <div className="border-l-4 border-brand-500 pl-4">
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">Personal Information</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>Email address (for account creation, order confirmations, and customer support)</li>
                  <li>Name (optional, for personalized experience)</li>
                  <li>Payment information (securely processed through Stripe and never stored on our servers)</li>
                  <li>Account preferences and settings</li>
                  <li>Communication preferences (newsletter, updates, promotional content)</li>
                </ul>
              </div>
              
              <div className="border-l-4 border-purple-500 pl-4">
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">AI Generation Data</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>Text prompts you provide for coloring page generation</li>
                  <li>Selected age groups, categories, and style preferences</li>
                  <li>Generated coloring page images and metadata</li>
                  <li>Generation history and usage patterns</li>
                  <li>Download history and preferences</li>
                  <li>Content feedback and ratings (when provided)</li>
                </ul>
                <p className="mt-2 text-sm text-purple-600 dark:text-purple-400">
                  <strong>Note:</strong> All prompts are automatically filtered for appropriateness before processing.
                </p>
              </div>

              <div className="border-l-4 border-green-500 pl-4">
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">Technical Information</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>IP address and approximate location (for security and service optimization)</li>
                  <li>Device information (browser type, operating system, screen resolution)</li>
                  <li>Usage analytics (pages visited, time spent, feature usage)</li>
                  <li>Performance data (loading times, error reports)</li>
                  <li>Cookies and similar tracking technologies</li>
                  <li>Session information and authentication tokens</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Lock className="h-5 w-5" /> 2. How We Use Your Information
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-50 dark:bg-surface-900 rounded-lg p-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">🎨 Service Delivery</h3>
                <ul className="list-disc pl-6 space-y-1 text-gray-700 dark:text-gray-300 text-sm">
                  <li>Generate AI-powered coloring pages based on your prompts</li>
                  <li>Process payments and manage subscription billing</li>
                  <li>Provide download access to generated content</li>
                  <li>Maintain your account and generation history</li>
                </ul>
              </div>
              <div className="bg-gray-50 dark:bg-surface-900 rounded-lg p-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">🔧 Service Improvement</h3>
                <ul className="list-disc pl-6 space-y-1 text-gray-700 dark:text-gray-300 text-sm">
                  <li>Analyze usage patterns to improve AI generation quality</li>
                  <li>Optimize website performance and user experience</li>
                  <li>Develop new features based on user needs</li>
                  <li>Ensure content safety and appropriateness</li>
                </ul>
              </div>
              <div className="bg-gray-50 dark:bg-surface-900 rounded-lg p-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">📧 Communication</h3>
                <ul className="list-disc pl-6 space-y-1 text-gray-700 dark:text-gray-300 text-sm">
                  <li>Send account-related notifications and updates</li>
                  <li>Provide customer support and technical assistance</li>
                  <li>Share educational content and tips (with consent)</li>
                  <li>Notify about new features and improvements</li>
                </ul>
              </div>
              <div className="bg-gray-50 dark:bg-surface-900 rounded-lg p-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">🛡️ Security & Compliance</h3>
                <ul className="list-disc pl-6 space-y-1 text-gray-700 dark:text-gray-300 text-sm">
                  <li>Prevent fraud and unauthorized access</li>
                  <li>Ensure compliance with legal obligations</li>
                  <li>Monitor for inappropriate content or misuse</li>
                  <li>Maintain service security and integrity</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Clock className="h-5 w-5" /> 3. Data Retention
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <p>We retain your information only for as long as necessary to fulfill the purposes outlined in this policy:</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {dataRetentionPeriods.map((item, index) => (
                  <div key={index} className="bg-gray-50 dark:bg-surface-900 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{item.category}</h3>
                    <p className="text-brand-600 dark:text-brand-400 font-medium mb-1">{item.period}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{item.description}</p>
                  </div>
                ))}
              </div>
              
              <div className="bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4 mt-4">
                <p className="text-amber-800 dark:text-amber-200 text-sm">
                  <strong>Note:</strong> You can request deletion of your data at any time through your account settings or by contacting our support team.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Cookie className="h-5 w-5" /> 4. Cookie Policy
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <p>We use cookies and similar technologies to enhance your experience:</p>
              
              <div className="space-y-4">
                {cookieTypes.map((type, index) => (
                  <div key={index} className="bg-gray-50 dark:bg-surface-900 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{type.type} Cookies</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{type.purpose}</p>
                    <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-2">
                      <Clock className="h-4 w-4" />
                      <span>Duration: {type.duration}</span>
                    </div>
                    <div className="text-sm">
                      <p className="font-medium text-gray-900 dark:text-white mb-1">Examples:</p>
                      <ul className="list-disc pl-6 space-y-1 text-gray-600 dark:text-gray-400">
                        {type.examples.map((example, i) => (
                          <li key={i}>{example}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mt-4">
                <p className="text-blue-800 dark:text-blue-200 text-sm">
                  <strong>Cookie Control:</strong> You can control cookie preferences through your browser settings. 
                  However, disabling certain cookies may affect the functionality of our service.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Globe className="h-5 w-5" /> 5. International Data Transfers
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <p>Your information may be transferred to and processed in countries other than your own:</p>
              
              <div className="bg-gray-50 dark:bg-surface-900 rounded-lg p-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Data Protection Standards</h3>
                <ul className="list-disc pl-6 space-y-2">
                  <li>We ensure appropriate safeguards are in place for international transfers</li>
                  <li>We comply with GDPR requirements for EU data transfers</li>
                  <li>We maintain data processing agreements with all service providers</li>
                  <li>We regularly review and update our data protection measures</li>
                </ul>
              </div>
              
              <div className="bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                <h3 className="font-semibold text-green-900 dark:text-green-100 mb-2">Your Rights Under GDPR</h3>
                <ul className="list-disc pl-6 space-y-1 text-green-800 dark:text-green-200">
                  <li>Right to access your personal data</li>
                  <li>Right to rectification of inaccurate data</li>
                  <li>Right to erasure ("right to be forgotten")</li>
                  <li>Right to data portability</li>
                  <li>Right to object to processing</li>
                  <li>Right to withdraw consent</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <FileText className="h-5 w-5" /> 6. Changes to This Policy
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <p>We may update this privacy policy from time to time. We will notify you of any changes by:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>Posting the new policy on this page</li>
                <li>Updating the "Last Updated" date</li>
                <li>Sending an email notification for significant changes</li>
                <li>Displaying a notice on our website</li>
              </ul>
              <p>We encourage you to review this policy periodically for any changes.</p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Mail className="h-5 w-5" /> 7. Contact Us
            </h2>
            <div className="bg-gray-50 dark:bg-surface-900 rounded-lg p-6">
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                If you have any questions about this Privacy Policy, please contact us:
              </p>
              <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                <li><strong>Email:</strong> <a href="mailto:privacy@thinkora.pics" className="text-brand-600 dark:text-brand-400 hover:underline">privacy@thinkora.pics</a></li>
                <li><strong>Support:</strong> <a href="mailto:support@thinkora.pics" className="text-brand-600 dark:text-brand-400 hover:underline">support@thinkora.pics</a></li>
                <li><strong>Data Protection Officer:</strong> <a href="mailto:dpo@thinkora.pics" className="text-brand-600 dark:text-brand-400 hover:underline">dpo@thinkora.pics</a></li>
              </ul>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;