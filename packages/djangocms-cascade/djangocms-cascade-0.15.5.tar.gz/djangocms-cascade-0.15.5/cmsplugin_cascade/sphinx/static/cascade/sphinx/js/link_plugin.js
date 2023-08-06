
django.jQuery(function($) {
	'use strict';

	django.cascade.SphinxDocsLinkPlugin = ring.create(eval(django.cascade.ring_plugin_bases.SphinxDocsLinkPlugin), {
		constructor: function() {
			this.$super();

			// be more intuitive, reorganize layout by moving 'Link Target'
			$('.glossary-widget .glossary_target').before($('.form-row.field-link_type'));
		},
		toggleLinkTypes: function(linkType) {
			var $field_cmspage = $(".form-row .field-box.field-cms_page, .form-row .field-box.field-section"),
				$field_documentation = $(".form-row .field-box.field-documentation"),
				$field_exturl = $(".form-row .field-box.field-ext_url"),
				$field_mailto = $(".form-row .field-box.field-mail_to"),
				$link_target = $(".glossary-widget.glossary_target");

			switch(linkType) {
			case 'cmspage':
				$field_cmspage.show();
				$field_documentation.hide();
				$field_exturl.hide();
				$field_mailto.hide();
				$link_target.hide();
				break;
			case 'documentation':
				$field_cmspage.hide();
				$field_documentation.show();
				$field_exturl.hide();
				$field_mailto.hide();
				$link_target.show();
				break;
			case 'exturl':
				$field_cmspage.hide();
				$field_documentation.hide();
				$field_exturl.show();
				$field_mailto.hide();
				$link_target.show();
				break;
			case 'email':
				$field_cmspage.hide();
				$field_documentation.hide();
				$field_exturl.hide();
				$field_mailto.show();
				$link_target.hide();
				break;
			default:
				$field_cmspage.hide();
				$field_documentation.hide();
				$field_exturl.hide();
				$field_mailto.hide();
				$link_target.hide();
				break;
			}
		}
	});
});
