<?php
/**
 * BuddyPress - Users Cover Image Header
 *
 * @package BuddyPress
 * @subpackage bp-legacy
 */

?>
<?php //@todo PP: Refactor to use the row markup. ?>
<div id="cover-image-container" class="g1-row-layout-page bp-layout-standard">

	<div id="header-cover-image">
		<?php if ( defined( 'BTP_DEV' ) && BTP_DEV && apply_filters( 'bimber_bp_show_profile_nav', true ) ) : ?>
			<?php
			$bimber_prev_id = bimber_bp_get_prev_user_id();
			$bimber_next_id = bimber_bp_get_next_user_id();
			?>
			<?php if ( $bimber_prev_id || $bimber_next_id ) : ?>
				<nav class="g1-bp-profile-nav">
					<?php if ( $bimber_prev_id ) : ?>
						<a class="g1-bp-profile-arrow g1-bp-profile-arrow-prev"
						   title="<?php esc_attr_e( 'Previous Member', 'bimber' ); ?>"
						   href="<?php echo esc_url( bp_core_get_user_domain( $bimber_prev_id ) ); ?>"
						   data-g1-member-id="<?php echo (int) $bimber_prev_id; ?>"
						>
							<?php
							echo bp_core_fetch_avatar( array(
								'item_id'   => $bimber_prev_id,
								'object'    => 'user',
								'width'     => 30,
								'height'    => 30,
								'class'     => 'avatar',
							) );
							?>
							<span class="g1-bp-profile-arrow-title"><?php echo bp_core_get_user_displayname( $bimber_prev_id ); ?></span>
						</a>
					<?php endif; ?>

					<?php if ( $bimber_next_id ) : ?>
						<a class="g1-bp-profile-arrow g1-bp-profile-arrow-next"
						   title="<?php esc_attr_e( 'Next Member', 'bimber' ); ?>"
						   href="<?php echo esc_url( bp_core_get_user_domain( $bimber_next_id ) ); ?>"
						   data-g1-member-id="<?php echo (int) $bimber_next_id; ?>"
						>
							<?php
							echo bp_core_fetch_avatar( array(
								'item_id'   => $bimber_next_id,
								'object'    => 'user',
								'width'     => 30,
								'height'    => 30,
								'class'     => 'avatar',
							) );
							?>
							<span class="g1-bp-profile-arrow-title"><?php echo bp_core_get_user_displayname( $bimber_next_id ); ?></span>
						</a>
					<?php endif; ?>

				</nav><!-- .g1-bp-profile-nav -->
			<?php endif; ?>
		<?php endif; ?>
	</div>

	<?php if ( bimber_bp_show_cover_image_change_link() ) : ?>
		<?php bimber_bp_render_cover_image_change_link(); ?>
	<?php endif; ?>

	<div id="item-header-cover-image">
	</div><!-- #item-header-cover-image -->

	<?php bp_get_template_part( 'members/single/member-header' ); ?>
</div><!-- #cover-image-container -->
