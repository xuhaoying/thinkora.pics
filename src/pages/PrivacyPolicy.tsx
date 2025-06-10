import React from 'react';
import { useTranslation } from 'react-i18next';

const PrivacyPolicy = () => {
  const { t } = useTranslation();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Privacy Policy</h1>
        
        <div className="prose prose-gray max-w-none">
          <p className="text-sm text-gray-600 mb-6">
            <strong>Effective Date:</strong> {new Date().toLocaleDateString()}
          </p>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">1. Information We Collect</h2>
            <div className="space-y-4 text-gray-700">
              <div>
                <h3 className="font-medium text-gray-900 mb-2">Personal Information</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>Email address (for account creation and communication)</li>
                  <li>Payment information (processed securely through our payment providers)</li>
                  <li>Usage preferences and settings</li>
                </ul>
              </div>
              
              <div>
                <h3 className="font-medium text-gray-900 mb-2">Generated Content</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>Text prompts you provide for AI coloring page generation</li>
                  <li>Generated coloring pages and associated metadata</li>
                  <li>Download and usage history</li>
                </ul>
              </div>

              <div>
                <h3 className="font-medium text-gray-900 mb-2">Technical Information</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>IP address and device information</li>
                  <li>Browser type and version</li>
                  <li>Usage analytics and performance data</li>
                  <li>Cookies and similar tracking technologies</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">2. How We Use Your Information</h2>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>To provide and improve our AI coloring page generation service</li>
              <li>To process payments and manage your account</li>
              <li>To communicate with you about your account and our services</li>
              <li>To analyze usage patterns and improve our service quality</li>
              <li>To prevent fraud and ensure service security</li>
              <li>To comply with legal obligations</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">3. Information Sharing</h2>
            <div className="space-y-4 text-gray-700">
              <p>We do not sell, trade, or rent your personal information to third parties. We may share information in the following limited circumstances:</p>
              <ul className="list-disc pl-6 space-y-1">
                <li><strong>Service Providers:</strong> With trusted third-party services that help us operate our platform (payment processing, hosting, analytics)</li>
                <li><strong>Legal Requirements:</strong> When required by law or to protect our rights and safety</li>
                <li><strong>Business Transfers:</strong> In the event of a merger, acquisition, or sale of assets</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">4. Data Security</h2>
            <div className="space-y-4 text-gray-700">
              <p>We implement industry-standard security measures to protect your information:</p>
              <ul className="list-disc pl-6 space-y-1">
                <li>Encryption of data in transit and at rest</li>
                <li>Secure payment processing through certified providers</li>
                <li>Regular security audits and updates</li>
                <li>Access controls and authentication measures</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">5. Your Rights and Choices</h2>
            <div className="space-y-4 text-gray-700">
              <p>You have the following rights regarding your personal information:</p>
              <ul className="list-disc pl-6 space-y-1">
                <li><strong>Access:</strong> Request access to your personal data</li>
                <li><strong>Correction:</strong> Request correction of inaccurate information</li>
                <li><strong>Deletion:</strong> Request deletion of your personal data</li>
                <li><strong>Portability:</strong> Request transfer of your data</li>
                <li><strong>Opt-out:</strong> Unsubscribe from marketing communications</li>
              </ul>
              <p>To exercise these rights, contact us at <a href="mailto:privacy@thinkora.pics" className="text-purple-600 hover:text-purple-700">privacy@thinkora.pics</a></p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">6. Cookies and Tracking</h2>
            <div className="space-y-4 text-gray-700">
              <p>We use cookies and similar technologies to:</p>
              <ul className="list-disc pl-6 space-y-1">
                <li>Remember your preferences and settings</li>
                <li>Analyze website performance and usage</li>
                <li>Provide personalized content and features</li>
              </ul>
              <p>You can control cookie settings through your browser preferences.</p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">7. Children's Privacy</h2>
            <p className="text-gray-700">
              While our coloring pages are designed for children, our service is intended for use by adults (parents, teachers, caregivers). 
              We do not knowingly collect personal information from children under 13. If you believe we have collected information 
              from a child under 13, please contact us immediately.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">8. International Data Transfers</h2>
            <p className="text-gray-700">
              Your information may be processed and stored in countries other than your own. We ensure appropriate safeguards 
              are in place to protect your data in accordance with applicable privacy laws.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">9. Data Retention</h2>
            <p className="text-gray-700">
              We retain your personal information only as long as necessary to provide our services and fulfill legal obligations. 
              Generated coloring pages are retained in your account until you delete them or close your account.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">10. Changes to This Policy</h2>
            <p className="text-gray-700">
              We may update this Privacy Policy from time to time. We will notify you of significant changes by email or 
              through our service. Your continued use of our service after changes take effect constitutes acceptance of the updated policy.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">11. Contact Information</h2>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-gray-700 mb-2">
                If you have questions about this Privacy Policy or our data practices, please contact us:
              </p>
              <ul className="text-gray-700 space-y-1">
                <li><strong>Email:</strong> <a href="mailto:privacy@thinkora.pics" className="text-purple-600 hover:text-purple-700">privacy@thinkora.pics</a></li>
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

export default PrivacyPolicy;