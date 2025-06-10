import React from 'react';
import { Scale, Shield, BookOpen, FileText, Mail, AlertTriangle, Users, CreditCard, Globe, Lock } from 'lucide-react';

const TermsOfService = () => {
  const licenseTypes = [
    {
      type: "Personal Use",
      description: "For individual use by parents, teachers, and caregivers",
      includes: [
        "Unlimited coloring page generation",
        "Personal printing and sharing",
        "Educational use in classrooms",
        "Non-commercial distribution"
      ]
    },
    {
      type: "Educational License",
      description: "For schools, educational institutions, and non-profit organizations",
      includes: [
        "All Personal Use features",
        "Multiple user accounts",
        "Bulk generation capabilities",
        "Educational resource sharing"
      ]
    },
    {
      type: "Commercial License",
      description: "For businesses and commercial use",
      includes: [
        "All Educational License features",
        "Commercial distribution rights",
        "White-label options",
        "API access (premium)"
      ]
    }
  ];

  const prohibitedContent = [
    {
      category: "Inappropriate Content",
      examples: [
        "Violent or graphic imagery",
        "Adult or mature themes",
        "Discriminatory content",
        "Hate speech or symbols"
      ]
    },
    {
      category: "Intellectual Property",
      examples: [
        "Copyrighted characters",
        "Trademarked logos",
        "Protected brand elements",
        "Licensed content"
      ]
    },
    {
      category: "Privacy & Safety",
      examples: [
        "Personal information",
        "Real people without consent",
        "Sensitive data",
        "Location-specific content"
      ]
    }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white dark:bg-surface-800 rounded-xl shadow-sm border border-gray-200 dark:border-surface-700 p-8">
        <div className="text-center mb-8">
          <div className="text-4xl mb-4">⚖️</div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Terms of Service</h1>
          <p className="text-gray-600 dark:text-gray-300">
            Please read these terms carefully before using our service
          </p>
        </div>
        
        <div className="prose prose-gray max-w-none dark:prose-invert">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 p-4 bg-gray-50 dark:bg-surface-900 rounded-lg">
            <strong>Effective Date:</strong> {new Date().toLocaleDateString()}
          </p>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Scale className="h-5 w-5" /> 1. Acceptance of Terms
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <p>
                By accessing and using Thinkora.pics ("the Service"), you accept and agree to be bound by the terms and 
                provision of this agreement. If you do not agree to abide by the above, please do not use this service.
              </p>
              <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <p className="text-blue-800 dark:text-blue-200 text-sm">
                  <strong>Important:</strong> These terms constitute a legally binding agreement between you and Thinkora.pics. 
                  By using our service, you acknowledge that you have read, understood, and agree to be bound by these terms.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <BookOpen className="h-5 w-5" /> 2. Service Description
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <p>Thinkora.pics provides an AI-powered coloring page generation service that allows users to:</p>
              <ul className="list-disc pl-6 space-y-1">
                <li>Generate custom coloring pages using artificial intelligence</li>
                <li>Download high-quality, print-ready coloring pages</li>
                <li>Access a library of generated content</li>
                <li>Customize generation parameters (age groups, styles, categories)</li>
              </ul>
              <p>This is a digital product service. All generated content is delivered digitally.</p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Users className="h-5 w-5" /> 3. User Accounts and Registration
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <ul className="list-disc pl-6 space-y-1">
                <li>You must provide accurate and complete information when creating an account</li>
                <li>You are responsible for maintaining the security of your account credentials</li>
                <li>You must be at least 18 years old to create an account</li>
                <li>One person or entity may not maintain multiple accounts</li>
                <li>You are responsible for all activities that occur under your account</li>
              </ul>
              <div className="bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
                <p className="text-amber-800 dark:text-amber-200 text-sm">
                  <strong>Security Note:</strong> If you suspect unauthorized access to your account, please contact our support team immediately.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <CreditCard className="h-5 w-5" /> 4. Pricing and Payment
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <h3 className="font-medium text-gray-900 dark:text-white">Payment Plans</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li><strong>Pay-per-page:</strong> $0.50 per generated coloring page</li>
                <li><strong>Monthly Unlimited:</strong> $9.90 per month for unlimited generations</li>
              </ul>
              
              <h3 className="font-medium text-gray-900 dark:text-white">Payment Terms</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li>All payments are processed securely through our payment providers</li>
                <li>Monthly subscriptions are billed automatically on your billing date</li>
                <li>All sales are final unless otherwise specified</li>
                <li>Prices are subject to change with 30 days notice</li>
                <li>We accept major credit cards and digital payment methods</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Shield className="h-5 w-5" /> 5. Acceptable Use Policy
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <p>You agree not to use the Service to:</p>
              <ul className="list-disc pl-6 space-y-1">
                <li>Generate inappropriate, offensive, or harmful content</li>
                <li>Create content that violates any laws or regulations</li>
                <li>Infringe on intellectual property rights of others</li>
                <li>Attempt to reverse engineer or hack the Service</li>
                <li>Share account credentials with others</li>
                <li>Use the Service for commercial purposes beyond personal/educational use without proper licensing</li>
                <li>Generate content depicting real people without consent</li>
                <li>Create content that promotes violence, discrimination, or illegal activities</li>
              </ul>

              <div className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <h3 className="font-semibold text-red-900 dark:text-red-100 mb-2">Prohibited Content Categories</h3>
                <div className="space-y-4">
                  {prohibitedContent.map((category, index) => (
                    <div key={index}>
                      <h4 className="font-medium text-red-800 dark:text-red-200 mb-1">{category.category}</h4>
                      <ul className="list-disc pl-6 space-y-1 text-red-700 dark:text-red-300">
                        {category.examples.map((example, i) => (
                          <li key={i}>{example}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <FileText className="h-5 w-5" /> 6. Licensing and Usage Rights
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {licenseTypes.map((license, index) => (
                  <div key={index} className="bg-gray-50 dark:bg-surface-900 rounded-lg p-6">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{license.type}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">{license.description}</p>
                    <ul className="space-y-2">
                      {license.includes.map((item, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm">
                          <span className="text-brand-500">✓</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
              
              <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <p className="text-blue-800 dark:text-blue-200 text-sm">
                  <strong>Note:</strong> For commercial use beyond the scope of these licenses, please contact our business development team.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Lock className="h-5 w-5" /> 7. Content Moderation and Safety
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <ul className="list-disc pl-6 space-y-1">
                <li>All generated content is filtered for appropriateness</li>
                <li>We reserve the right to review and remove content that violates our policies</li>
                <li>Content is designed to be safe and appropriate for children</li>
                <li>We use automated and manual review processes to ensure content quality</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" /> 8. Refunds and Cancellations
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <h3 className="font-medium text-gray-900 dark:text-white">Monthly Subscriptions</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li>Cancel anytime before your next billing cycle</li>
                <li>No refunds for partial months</li>
                <li>Access continues until the end of your paid period</li>
              </ul>
              
              <h3 className="font-medium text-gray-900 dark:text-white">Pay-per-page</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li>Refunds available if technical issues prevent content generation</li>
                <li>No refunds for successfully generated content</li>
                <li>Contact support within 24 hours for technical issues</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Globe className="h-5 w-5" /> 9. Service Availability
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <ul className="list-disc pl-6 space-y-1">
                <li>We strive for 99.9% uptime but cannot guarantee uninterrupted service</li>
                <li>Scheduled maintenance will be announced in advance when possible</li>
                <li>We are not liable for service interruptions beyond our control</li>
                <li>Generation times may vary based on system load and complexity</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Scale className="h-5 w-5" /> 10. Limitation of Liability
            </h2>
            <p className="text-gray-700 dark:text-gray-300">
              To the maximum extent permitted by law, Thinkora.pics shall not be liable for any indirect, incidental, 
              special, consequential, or punitive damages, including without limitation, loss of profits, data, use, 
              goodwill, or other intangible losses, resulting from your use of the Service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" /> 11. Termination
            </h2>
            <div className="space-y-4 text-gray-700 dark:text-gray-300">
              <p>We may terminate or suspend your account and access to the Service immediately, without prior notice, for:</p>
              <ul className="list-disc pl-6 space-y-1">
                <li>Violation of these Terms of Service</li>
                <li>Fraudulent or illegal activity</li>
                <li>Non-payment of fees</li>
                <li>Abuse of the Service or other users</li>
              </ul>
              <p>Upon termination, your right to use the Service ceases immediately.</p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <FileText className="h-5 w-5" /> 12. Changes to Terms
            </h2>
            <p className="text-gray-700 dark:text-gray-300">
              We reserve the right to modify these terms at any time. We will notify users of significant changes 
              by email or through the Service. Continued use of the Service after changes constitutes acceptance 
              of the new terms.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Globe className="h-5 w-5" /> 13. Governing Law
            </h2>
            <p className="text-gray-700 dark:text-gray-300">
              These Terms shall be governed by and construed in accordance with the laws of [Your Jurisdiction], 
              without regard to its conflict of law provisions.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Mail className="h-5 w-5" /> 14. Contact Information
            </h2>
            <div className="bg-gray-50 dark:bg-surface-900 p-4 rounded-lg">
              <p className="text-gray-700 dark:text-gray-300 mb-2">
                For questions about these Terms of Service, please contact us:
              </p>
              <ul className="text-gray-700 dark:text-gray-300 space-y-1">
                <li><strong>Email:</strong> <a href="mailto:legal@thinkora.pics" className="text-brand-600 dark:text-brand-400 hover:underline">legal@thinkora.pics</a></li>
                <li><strong>Support:</strong> <a href="mailto:support@thinkora.pics" className="text-brand-600 dark:text-brand-400 hover:underline">support@thinkora.pics</a></li>
                <li><strong>Business Address:</strong> [Your Business Address]</li>
              </ul>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default TermsOfService;