import React from 'react';

const TermsOfService = () => {

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Terms of Service</h1>
        
        <div className="prose prose-gray max-w-none">
          <p className="text-sm text-gray-600 mb-6">
            <strong>Effective Date:</strong> {new Date().toLocaleDateString()}
          </p>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">1. Acceptance of Terms</h2>
            <p className="text-gray-700">
              By accessing and using Thinkora.pics ("the Service"), you accept and agree to be bound by the terms and 
              provision of this agreement. If you do not agree to abide by the above, please do not use this service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">2. Service Description</h2>
            <div className="space-y-4 text-gray-700">
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
            <h2 className="text-xl font-semibold text-gray-900 mb-4">3. User Accounts and Registration</h2>
            <div className="space-y-4 text-gray-700">
              <ul className="list-disc pl-6 space-y-1">
                <li>You must provide accurate and complete information when creating an account</li>
                <li>You are responsible for maintaining the security of your account credentials</li>
                <li>You must be at least 18 years old to create an account</li>
                <li>One person or entity may not maintain multiple accounts</li>
                <li>You are responsible for all activities that occur under your account</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">4. Pricing and Payment</h2>
            <div className="space-y-4 text-gray-700">
              <h3 className="font-medium text-gray-900">Payment Plans</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li><strong>Pay-per-page:</strong> $0.50 per generated coloring page</li>
                <li><strong>Monthly Unlimited:</strong> $9.90 per month for unlimited generations</li>
              </ul>
              
              <h3 className="font-medium text-gray-900">Payment Terms</h3>
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
            <h2 className="text-xl font-semibold text-gray-900 mb-4">5. Acceptable Use Policy</h2>
            <div className="space-y-4 text-gray-700">
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
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">6. Intellectual Property Rights</h2>
            <div className="space-y-4 text-gray-700">
              <h3 className="font-medium text-gray-900">Your Content</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li>You retain rights to the text prompts you provide</li>
                <li>Generated coloring pages are owned by you for personal and educational use</li>
                <li>Commercial use of generated content may require additional licensing</li>
              </ul>
              
              <h3 className="font-medium text-gray-900">Our Content</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li>The Service, including AI models, software, and website, is our intellectual property</li>
                <li>You may not copy, modify, or distribute our proprietary technology</li>
                <li>Our trademarks and branding are protected and may not be used without permission</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">7. Content Moderation and Safety</h2>
            <div className="space-y-4 text-gray-700">
              <ul className="list-disc pl-6 space-y-1">
                <li>All generated content is filtered for appropriateness</li>
                <li>We reserve the right to review and remove content that violates our policies</li>
                <li>Content is designed to be safe and appropriate for children</li>
                <li>We use automated and manual review processes to ensure content quality</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">8. Refunds and Cancellations</h2>
            <div className="space-y-4 text-gray-700">
              <h3 className="font-medium text-gray-900">Monthly Subscriptions</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li>Cancel anytime before your next billing cycle</li>
                <li>No refunds for partial months</li>
                <li>Access continues until the end of your paid period</li>
              </ul>
              
              <h3 className="font-medium text-gray-900">Pay-per-page</h3>
              <ul className="list-disc pl-6 space-y-1">
                <li>Refunds available if technical issues prevent content generation</li>
                <li>No refunds for successfully generated content</li>
                <li>Contact support within 24 hours for technical issues</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">9. Service Availability</h2>
            <div className="space-y-4 text-gray-700">
              <ul className="list-disc pl-6 space-y-1">
                <li>We strive for 99.9% uptime but cannot guarantee uninterrupted service</li>
                <li>Scheduled maintenance will be announced in advance when possible</li>
                <li>We are not liable for service interruptions beyond our control</li>
                <li>Generation times may vary based on system load and complexity</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">10. Limitation of Liability</h2>
            <p className="text-gray-700">
              To the maximum extent permitted by law, Thinkora.pics shall not be liable for any indirect, incidental, 
              special, consequential, or punitive damages, including without limitation, loss of profits, data, use, 
              goodwill, or other intangible losses, resulting from your use of the Service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">11. Termination</h2>
            <div className="space-y-4 text-gray-700">
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
            <h2 className="text-xl font-semibold text-gray-900 mb-4">12. Changes to Terms</h2>
            <p className="text-gray-700">
              We reserve the right to modify these terms at any time. We will notify users of significant changes 
              by email or through the Service. Continued use of the Service after changes constitutes acceptance 
              of the new terms.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">13. Governing Law</h2>
            <p className="text-gray-700">
              These Terms shall be governed by and construed in accordance with the laws of [Your Jurisdiction], 
              without regard to its conflict of law provisions.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">14. Contact Information</h2>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-gray-700 mb-2">
                For questions about these Terms of Service, please contact us:
              </p>
              <ul className="text-gray-700 space-y-1">
                <li><strong>Email:</strong> <a href="mailto:legal@thinkora.pics" className="text-purple-600 hover:text-purple-700">legal@thinkora.pics</a></li>
                <li><strong>Support:</strong> <a href="mailto:support@thinkora.pics" className="text-purple-600 hover:text-purple-700">support@thinkora.pics</a></li>
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