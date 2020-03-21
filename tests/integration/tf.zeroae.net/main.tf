module "file-cache" {
  source = "tf.zeroae.net/plus3it/file-cache/external"
  version = "1.2.0"
}

module "file-cache-latest" {
  source = "tf.zeroae.net/plus3it/file-cache/external"
  # version = "1.3.1"
}

module "file-cache-ranged" {
  source = "tf.zeroae.net/plus3it/file-cache/external"
  version = ">=1.3.0"
}

module "file-cache-older" {
  source = "tf.zeroae.net/plus3it/file-cache/external"
  version = "~>1.2.0"
}
