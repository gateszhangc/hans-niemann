#!/usr/bin/env bash
set -euo pipefail

export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export WEBAPP_LAUNCH_ANALYTICS_SKILL_DIR="${WEBAPP_LAUNCH_ANALYTICS_SKILL_DIR:-$CODEX_HOME/skills/webapp-launch-analytics}"
export PATH="$(dirname "$0")/bin:$PATH"

export PRIMARY_URL="https://hans-niemann.lol"
export PRIMARY_DOMAIN_LOCK="hans-niemann.lol"
export PROJECT_NAME="hans-niemann"
export SEO_PRIMARY_KEYWORD="hans niemann"

export GITHUB_CREATE_REPO="never"
export GITHUB_OWNER="gateszhangc"
export GITHUB_REPO="hans-niemann"
export GITHUB_VISIBILITY="public"
export DEPLOY_GIT_BRANCH="main"
export GIT_AUTO_COMMIT_BEFORE_PUSH="true"
export GIT_AUTO_COMMIT_MESSAGE="chore: sync launch analytics updates"
export GITHUB_RELEASE_WORKFLOW_NAME="Build And Release"
export WAIT_FOR_GITHUB_RELEASE_WORKFLOW="true"

export IMAGE_REGISTRY="registry.144.91.77.245.sslip.io"
export IMAGE_REPOSITORY="registry.144.91.77.245.sslip.io/hans-niemann"
export K8S_ROOT="deploy/k8s"
export K8S_NAMESPACE="hans-niemann"
export APP_PORT="8080"
export SERVICE_PORT="80"
export INGRESS_CLASS_NAME="nginx"
export CERT_MANAGER_CLUSTER_ISSUER="letsencrypt-prod"
export IMAGE_PULL_SECRET_NAME="dokploy-fleet-ghcr"
export ARGOCD_APPLICATION_NAME="hans-niemann"
export ARGOCD_NAMESPACE="argocd"

export ENABLE_CLOUDFLARE_DNS_MIGRATION="true"
export CLOUDFLARE_ACCOUNT_ID="45a8243cc61a1d87d62200124ab0c311"
export DNS_PROVIDER="porkbun"
export PORKBUN_NS_MODE="api"
export DNS_TARGET_APEX_IP="89.167.61.228"
export DNS_TARGET_WWW="hans-niemann.lol"
export CLOUDFLARE_PROXY_APEX="false"
export CLOUDFLARE_PROXY_WWW="false"

export GOOGLE_AUTH_MODE="${GOOGLE_AUTH_MODE:-adc_user_only}"
export GOOGLE_REQUIRED_USER_EMAIL="${GOOGLE_REQUIRED_USER_EMAIL:-gateszhang92@gmail.com}"
export GOOGLE_USER_PROJECT="${GOOGLE_USER_PROJECT:-ai-outfit-generator-480107}"
export GA4_CREATE_MODE="create_new"
export GA4_PROPERTY_DISPLAY_NAME="Hans Niemann"
export CLARITY_PROJECT_ID="wbzx6vuhvd"
export DEV_ENV_FILE=".env.development"
export PROD_ENV_FILE=".env.production"
export SKIP_GSC="false"
export SKIP_GA4="true"
export SKIP_CLARITY="false"
export SKIP_SEO_KEYWORD_CHECK="true"
export SKIP_DB_INIT="true"
export SKIP_DB_SCHEMA_SYNC="true"

cd "$(dirname "$0")/../../.."

bash "$WEBAPP_LAUNCH_ANALYTICS_SKILL_DIR/scripts/release-via-argo-and-verify.sh" \
  origin \
  main \
  hans-niemann \
  https://hans-niemann.lol
